using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using SafariSalama.API.Models;
using SafariSalama.API.DTOs;

namespace SafariSalama.API.Controllers
{
    [Authorize(Roles = "admin")]
    [ApiController]
    [Route("api/[controller]")]
    public class AdminController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public AdminController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet("guardians")]
        public async Task<ActionResult<IEnumerable<GuardianDto>>> GetGuardians()
        {
            var guardians = await _context.Guardians
                .Select(g => new GuardianDto
                {
                    Id = g.Id,
                    Name = g.Name,
                    Email = g.Email,
                    PhoneNumber = g.PhoneNumber,
                    Address = g.Address
                })
                .ToListAsync();

            return Ok(guardians);
        }

        [HttpGet("students")]
        public async Task<ActionResult<IEnumerable<StudentDto>>> GetStudents()
        {
            var students = await _context.Students
                .Include(s => s.Guardian)
                .Include(s => s.Bus)
                .Select(s => new { s.Id, s.Name, s.Grade, Guardian = s.Guardian, Bus = s.Bus, s.Status, s.LastUpdate })
                .ToListAsync();

            var studentDtos = students.Select(s => new StudentDto
            {
                Id = s.Id,
                Name = s.Name,
                Grade = s.Grade,
                GuardianName = s.Guardian != null ? s.Guardian.Name : "No Guardian",
                BusNumber = s.Bus != null ? s.Bus.Number : "Unassigned",
                Status = s.Status,
                LastUpdate = s.LastUpdate
            }).ToList();

            return Ok(studentDtos);
        }

        [HttpGet("buses")]
        public async Task<ActionResult<IEnumerable<BusDto>>> GetBuses()
        {
            var buses = await _context.Buses
                .Include(b => b.Driver)
                .Include(b => b.Attendant)
                .Select(b => new { b.Id, b.Number, b.Capacity, Driver = b.Driver, b.Status })
                .ToListAsync();

            var busDtos = buses.Select(b => new BusDto
            {
                Id = b.Id,
                Number = b.Number,
                Capacity = b.Capacity,
                DriverName = b.Driver != null ? b.Driver.Name : "Unassigned",
                Status = b.Status
            }).ToList();

            return Ok(busDtos);
        }

        [HttpPost("bus")]
        public async Task<ActionResult<BusDto>> CreateBus(CreateBusDto busDto)
        {
            var bus = new Bus
            {
                Number = busDto.Number,
                Capacity = busDto.Capacity,
                Status = "Available"
            };

            _context.Buses.Add(bus);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetBuses), new { id = bus.Id }, bus);
        }

        [HttpPost("student")]
        public async Task<ActionResult<StudentDto>> CreateStudent(CreateStudentDto studentDto)
        {
            var student = new Student
            {
                Name = studentDto.Name,
                Grade = studentDto.Grade,
                GuardianId = studentDto.GuardianId,
                BusId = studentDto.BusId,
                Status = "Not on bus"
            };

            _context.Students.Add(student);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetStudents), new { id = student.Id }, student);
        }
    }
}
