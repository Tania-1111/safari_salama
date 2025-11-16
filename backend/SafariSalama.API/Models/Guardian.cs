using System.ComponentModel.DataAnnotations;

namespace SafariSalama.API.Models
{
    public class Guardian
    {
        [Key]
        public int Id { get; set; }
        [Required] public string Name { get; set; } = string.Empty;
        [Required] public string Email { get; set; } = string.Empty;
        [Required] public string PasswordHash { get; set; } = string.Empty;
        [Required] public string PhoneNumber { get; set; } = string.Empty;
        [Required] public string Address { get; set; } = string.Empty;

        public ICollection<Student> Students { get; set; } = new List<Student>();
        public string Role { get; set; } = "guardian";
    }
}