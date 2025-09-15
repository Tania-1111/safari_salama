namespace SafariSalama.API.DTOs
{
    public class StudentDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Grade { get; set; } = string.Empty;
        public string GuardianName { get; set; } = string.Empty;
        public string BusNumber { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public DateTime LastUpdate { get; set; }
    }

    public class GuardianDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string PhoneNumber { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
    }

    public class BusDto
    {
        public int Id { get; set; }
        public string Number { get; set; } = string.Empty;
        public int Capacity { get; set; }
        public string DriverName { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
    }

    public class TripDto
    {
        public int Id { get; set; }
        public string BusNumber { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public LocationDto CurrentLocation { get; set; } = null!;
        public DateTime EstimatedArrival { get; set; }
    }

    public class LocationDto
    {
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }
}
