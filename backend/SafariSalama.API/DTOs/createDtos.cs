namespace SafariSalama.API.DTOs
{
    public class CreateStudentDto
    {
        public string Name { get; set; } = string.Empty;
        public string Grade { get; set; } = string.Empty;
        public int GuardianId { get; set; }
        public int? BusId { get; set; }
    }

    public class CreateBusDto
    {
        public string Number { get; set; } = string.Empty;
        public int Capacity { get; set; } = 50;
    }

    public class CreateBusAttendantDto
    {
        public string Name { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public int? BusId { get; set; }
    }

    public class CreateDriverDto
    {
        public string Name { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public int? BusId { get; set; }
    }
}
