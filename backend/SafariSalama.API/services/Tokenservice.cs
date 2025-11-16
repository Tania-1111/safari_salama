using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using SafariSalama.API.Models;

namespace SafariSalama.API.Services
{
    public class TokenService : ITokenService
    {
        private readonly IConfiguration _configuration;

        public TokenService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public string CreateToken(Guardian guardian)
        {
            var claims = new List<Claim>
            {
                new Claim("id", guardian.Id.ToString()),
                new Claim("email", guardian.Email),
                new Claim("name", guardian.Name),
                new Claim(ClaimTypes.Role, "guardian")
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(
                _configuration["JwtSettings:SecretKey"] ?? 
                throw new InvalidOperationException("JWT Secret key is not configured")));

            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);

            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Subject = new ClaimsIdentity(claims),
                Expires = DateTime.UtcNow.AddDays(
                    double.Parse(_configuration["JwtSettings:ExpiryInDays"] ?? "7")),
                SigningCredentials = creds
            };

            var tokenHandler = new JwtSecurityTokenHandler();
            var token = tokenHandler.CreateToken(tokenDescriptor);

            return tokenHandler.WriteToken(token);
        }
    }
}
