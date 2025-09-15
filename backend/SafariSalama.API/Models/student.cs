using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SafariSalama.API.Models
{
    public class Student
    {
        [Key]
        public int Id { get; set; }

        [Required] public string Name { get; set; } = string.Empty;
        [Required] public string Grade { get; set; } = string.Empty;
        public string Status { get; set; } = "Not on bus";
        public DateTime LastUpdate { get; set; } = DateTime.UtcNow;

        [ForeignKey("Guardian")]
        public int GuardianId { get; set; }
        public Guardian? Guardian { get; set; }

        public int? BusId { get; set; }
        public Bus? Bus { get; set; }
    }
}
