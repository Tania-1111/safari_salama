using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using SafariSalama.API.Services;
using SafariSalama.API.Models;
using SafariSalama.API.DTOs;

namespace SafariSalama.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly ITokenService _tokenService;
        private readonly ApplicationDbContext _context;

        public AuthController(ITokenService tokenService, ApplicationDbContext context)
        {
            _tokenService = tokenService;
            _context = context;
        }

        [HttpPost("register")]
        public async Task<ActionResult<AuthResponseDto>> Register(RegisterDto registerDto)
        {
            // Check if user already exists
            if (await _context.Guardians.AnyAsync(x => x.Email == registerDto.Email))
            {
                return BadRequest("Email already exists");
            }

            // Create new guardian
            var guardian = new Guardian
            {
                Name = registerDto.Name,
                Email = registerDto.Email,
                PasswordHash = BCrypt.Net.BCrypt.EnhancedHashPassword(registerDto.Password),
                PhoneNumber = registerDto.PhoneNumber,
                Address = registerDto.Address
            };

            _context.Guardians.Add(guardian);
            await _context.SaveChangesAsync();

            // Generate token
            var token = _tokenService.CreateToken(guardian);

            return new AuthResponseDto
            {
                Token = token,
                User = new UserDto
                {
                    Id = guardian.Id,
                    Name = guardian.Name,
                    Email = guardian.Email,
                    Role = "guardian"
                }
            };
        }

        [HttpPost("login")]
        public async Task<ActionResult<AuthResponseDto>> Login(LoginDto loginDto)
        {
            // Find guardian
            var guardian = await _context.Guardians
                .FirstOrDefaultAsync(x => x.Email == loginDto.Email);

            if (guardian == null || !BCrypt.Net.BCrypt.EnhancedVerify(loginDto.Password, guardian.PasswordHash))
            {
                return Unauthorized("Invalid email or password");
            }

            // Generate token
            var token = _tokenService.CreateToken(guardian);

            return new AuthResponseDto
            {
                Token = token,
                User = new UserDto
                {
                    Id = guardian.Id,
                    Name = guardian.Name,
                    Email = guardian.Email,
                    Role = "guardian"
                }
            };
        }
    }
}
