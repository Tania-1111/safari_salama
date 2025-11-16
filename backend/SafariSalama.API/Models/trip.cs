using System.ComponentModel.DataAnnotations;

namespace SafariSalama.API.Models
{
    public class Trip
    {
        [Key]
        public int Id { get; set; }

        public int BusId { get; set; }
        public Bus? Bus { get; set; }

        public string Status { get; set; } = "Scheduled";
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public DateTime EstimatedArrival { get; set; }

        public double CurrentLatitude { get; set; }
        public double CurrentLongitude { get; set; }
        public DateTime LastLocationUpdate { get; set; } = DateTime.UtcNow;
    }
}
