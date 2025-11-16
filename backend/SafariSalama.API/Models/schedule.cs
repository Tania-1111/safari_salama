using System.ComponentModel.DataAnnotations;

namespace SafariSalama.API.Models
{
    public class Schedule
    {
        [Key]
        public int Id { get; set; }

        public int BusId { get; set; }
        public Bus? Bus { get; set; }

        public DateTime PickupTime { get; set; }
        public DateTime DropoffTime { get; set; }
        public string? StopName { get; set; }
        public double? Latitude { get; set; }
        public double? Longitude { get; set; }
    }
}
