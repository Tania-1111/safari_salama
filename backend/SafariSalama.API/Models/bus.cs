using System.ComponentModel.DataAnnotations;

namespace SafariSalama.API.Models
{
    public class Bus
    {
        [Key]
        public int Id { get; set; }

        [Required] public string Number { get; set; } = string.Empty;
        public int Capacity { get; set; } = 50;
        public string Status { get; set; } = "Available";

        public int? DriverId { get; set; }
        public Driver? Driver { get; set; }

        public int? AttendantId { get; set; }
        public BusAttendant? Attendant { get; set; }

        public ICollection<Trip> Trips { get; set; } = new List<Trip>();
        public ICollection<Student> Students { get; set; } = new List<Student>();
    }
}
