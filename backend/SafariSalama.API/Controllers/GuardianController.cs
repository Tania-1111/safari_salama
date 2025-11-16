using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using SafariSalama.API.Models;
using SafariSalama.API.DTOs;

namespace SafariSalama.API.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/[controller]")]
    public class GuardianController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public GuardianController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet("students")]
        public async Task<ActionResult<IEnumerable<StudentDto>>> GetStudents()
        {
            var guardianId = int.Parse(User.FindFirst("id")?.Value ?? "0");
            
            var students = await _context.Students
                .Where(s => s.GuardianId == guardianId)
                .Select(s => new { s.Id, s.Name, s.Grade, Bus = s.Bus, s.Status, s.LastUpdate })
                .ToListAsync();

            var studentDtos = students.Select(s => new StudentDto
            {
                Id = s.Id,
                Name = s.Name,
                Grade = s.Grade,
                BusNumber = s.Bus != null ? s.Bus.Number : "Unassigned",
                Status = s.Status,
                LastUpdate = s.LastUpdate
            }).ToList();

            return Ok(studentDtos);
        }

        [HttpGet("trips")]
        public async Task<ActionResult<IEnumerable<TripDto>>> GetTrips()
        {
            var guardianId = int.Parse(User.FindFirst("id")?.Value ?? "0");
            
            var trips = await _context.Trips
                .Include(t => t.Bus)
                .Where(t => t.Bus != null)
                .Where(t => t.Bus.Students.Any(s => s.GuardianId == guardianId))
                .Select(t => new { t.Id, Bus = t.Bus, t.Status, t.CurrentLatitude, t.CurrentLongitude, t.EstimatedArrival })
                .ToListAsync();

            var tripDtos = trips.Select(t => new TripDto
            {
                Id = t.Id,
                BusNumber = t.Bus != null ? t.Bus.Number : "Unknown",
                Status = t.Status,
                CurrentLocation = new LocationDto
                {
                    Latitude = t.CurrentLatitude,
                    Longitude = t.CurrentLongitude
                },
                EstimatedArrival = t.EstimatedArrival
            }).ToList();

            return Ok(tripDtos);
        }
    }
}
