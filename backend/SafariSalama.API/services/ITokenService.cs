using SafariSalama.API.Models;

namespace SafariSalama.API.Services
{
    public interface ITokenService
    {
        string CreateToken(Guardian guardian);
    }
}
