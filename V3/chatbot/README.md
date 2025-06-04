a bit out-of-scope for this term improvements:
- multi format support
- performance improvements:
	- can use API calls for significantly lower latency in token generation
		- openrouter is a great choice
- multi-user multi-gpu support for larger infrastuctures 
	- ollama is only for easy-to-use interface and single-use enviromemns
		- vLLM can be used for this purpose (though more complex)
- faster embedding/similarity search when accessing vector dBs
- in the dB section:
	- the dB can be further improved to separate out department wise handling
		- i.e, managing separate vector dBs for internal docs of different departments and a common dB for general purpose use by everyone (guidelines and shi)

- user authentication
- support for long-term memory

P.S: implementing and successfully running all this will take significantly more time and efforts
