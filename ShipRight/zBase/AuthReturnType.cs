using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ShipRight.zBase
{
	public class AuthReturnType
	{
		[JsonProperty("ah")]
		public string Hash { get; set; }

		[JsonProperty("av")]
		public int Offset { get; set; }
	}
}
