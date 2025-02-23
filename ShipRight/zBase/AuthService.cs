using Newtonsoft.Json;
using System;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ShipRight.zBase
{
	[System.Reflection.Obfuscation(Feature = "Virtualization", Exclude = false)]
	internal class AuthService
	{
		private MainForm MainForm { get; }
		private string authCode;
		private const int maxMissed = 3;
		private string queryString;
		private readonly string sessionId;
		private readonly IConfiguration _configuration;
		private int missed = 0;

		public AuthService(MainForm mainForm, IConfiguration configuration)
		{
			sessionId = Guid.NewGuid().ToString();
			MainForm = mainForm;
			_configuration = configuration;
			RunPeriodically();
			Run();
		}

		[System.Reflection.Obfuscation(Feature = "Virtualization", Exclude = false)]
		private void Run()
		{
			var client = new HttpClient();
			authCode = File.ReadAllText(Directory.GetFiles(Directory.GetCurrentDirectory()).First(x => x.EndsWith("authcode.txt")));

			queryString = $"https://api.barrelstopper.com/Authenticator/Authenticate/ShipRight?token={authCode}";
			var cla = Environment.GetCommandLineArgs();

			var resultString = client
				.PostAsync(queryString, new StringContent(JsonConvert.SerializeObject(new AuthParams
				{
					g = authCode,
					a = true,
					b = MainForm.ClientName,
					c = NetworkInterface
						.GetAllNetworkInterfaces()
						.Where(nic => nic.OperationalStatus == OperationalStatus.Up &&
									  nic.NetworkInterfaceType != NetworkInterfaceType.Loopback)
						.Select(nic => nic.GetPhysicalAddress().ToString())
						.FirstOrDefault(),
					d = MainForm.BotVersion,
					e = sessionId,
					f = File.Exists($"{Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData)}/hash.dat")
						? File.ReadAllText($"{Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData)}/hash.dat")
						: "UNKNOWN"
				}), Encoding.UTF8, "application/json")) // TODO: Add more stuff in the future. 
				.Result
				.Content
				.ReadAsStringAsync()
				.Result;

			var result = JsonConvert.DeserializeObject<AuthReturnType>(resultString);

			if (result.Hash != string.Concat(System.Security.Cryptography.SHA256.Create()
					.ComputeHash(Encoding.UTF8.GetBytes($"mZq4t7w!z$C&F)J@NcRfUjXn2r5u8x/A{sessionId}"))
					.Select(item => item.ToString("x2")))) throw new Exception();

			_configuration.AuthValue = result.Offset;

			Application.Run(MainForm);
		}

		[System.Reflection.Obfuscation(Feature = "Virtualization", Exclude = false)]
		private void FuckOff()
		{
			var client = new HttpClient();

			var result = JsonConvert.DeserializeObject<AuthReturnType>(client
				.PostAsync(queryString, new StringContent(JsonConvert.SerializeObject(new AuthParams
				{
					g = authCode,
					a = true,
					b = MainForm.ClientName,
					c = NetworkInterface
						.GetAllNetworkInterfaces()
						.Where(nic => nic.OperationalStatus == OperationalStatus.Up && nic.NetworkInterfaceType != NetworkInterfaceType.Loopback)
						.Select(nic => nic.GetPhysicalAddress().ToString())
						.FirstOrDefault(),
					d = MainForm.BotVersion,
					e = sessionId,
					f = File.Exists($"{Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData)}/hash.dat")
						? File.ReadAllText($"{Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData)}/hash.dat")
						: "UNKNOWN"
				}), Encoding.UTF8, "application/json")) // TODO: Add more stuff in the future. 
				.Result
				.Content
				.ReadAsStringAsync()
				.Result);

			if (result.Hash != string.Concat(System.Security.Cryptography.SHA256.Create()
					.ComputeHash(Encoding.UTF8.GetBytes($"mZq4t7w!z$C&F)J@NcRfUjXn2r5u8x/A{sessionId}"))
					.Select(item => item.ToString("x2"))))
			{
				missed++;

				if (missed >= maxMissed)
				{
					MainForm.Close();
				}
			}
			else
			{
				missed = 0;
			}

		}

		private async Task RunPeriodically()
		{
			var ctx = new CancellationToken();

			await Task.Delay(TimeSpan.FromSeconds(10), ctx);

			while (true)
			{
				FuckOff();
				await Task.Delay(TimeSpan.FromMinutes(5), ctx);
			}
		}
	}

}
