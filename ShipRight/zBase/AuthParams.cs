using Newtonsoft.Json;

namespace ShipRight.zBase
{
	public class AuthParams
	{
		[JsonProperty(PropertyName = "g")]
		public string g { get; set; }

		[JsonProperty(PropertyName = "a")]
		public bool a { get; set; }

		[JsonProperty(PropertyName = "b")]
		public string b { get; set; }

		[JsonProperty(PropertyName = "c")]
		public string c { get; set; }

		[JsonProperty(PropertyName = "d")]
		public string d { get; set; }

		[JsonProperty(PropertyName = "e")]
		public string e { get; set; }

		[JsonProperty(PropertyName = "f")]
		public string f { get; set; }
	}
}
