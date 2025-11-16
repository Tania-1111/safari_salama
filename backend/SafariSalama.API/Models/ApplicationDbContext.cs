using Microsoft.EntityFrameworkCore;

namespace SafariSalama.API.Models
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) {}
        public DbSet<Guardian> Guardians { get; set; } = null!;
        public DbSet<Student> Students { get; set; } = null!;
        public DbSet<Bus> Buses { get; set; } = null!;
        public DbSet<Driver> Drivers { get; set; } = null!;
        public DbSet<Schedule> Schedules { get; set; } = null!;
        public DbSet<Trip> Trips { get; set; } = null!;
        public DbSet<BusAttendant> BusAttendants { get; set; } = null!;
        // public DbSet<Admin> Admins { get; set; } = null!;
    
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Guardian>()
                .HasMany(g => g.Students)
                .WithOne(s => s.Guardian)
                .HasForeignKey(s => s.GuardianId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Bus>()
                .HasOne(b => b.Driver)
                .WithOne(d => d.Bus)
                .HasForeignKey<Driver>(d => d.BusId)
                .OnDelete(DeleteBehavior.SetNull);   

           modelBuilder.Entity<Bus>()
                 .HasOne(b => b.Attendant)
                 .WithOne(a => a.Bus)
                 .HasForeignKey<BusAttendant>(a => a.BusId)
                 .OnDelete(DeleteBehavior.SetNull); 

            modelBuilder.Entity<Bus>()
                .HasMany(b => b.Trips)
                .WithOne(t => t.Bus)
                .HasForeignKey(t => t.BusId)
                .OnDelete(DeleteBehavior.Cascade);

            base.OnModelCreating(modelBuilder);     
        }
    
    }
}
