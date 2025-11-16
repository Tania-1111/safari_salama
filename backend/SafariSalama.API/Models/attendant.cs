using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SafariSalama.API.Models
{
    public class BusAttendant
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string Name { get; set; } = string.Empty;
        
        [Required]
        public string Phone { get; set; } = string.Empty;

        public int? BusId { get; set; }
        public Bus? Bus { get; set; }
    }
}
