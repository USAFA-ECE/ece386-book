# Final: Integration

At this point the components are nearly done!

Time to connect them 😈

## Debugging Tips

Here are some known "gotchas." You should really read them all.

If you have one to add, please [edit and submit a pull request](https://github.com/USAFA-ECE/ece386-book/blob/main/book/b5-final/integration.md)!

### Docker

#### Can't connect to DFEC AI server

The DFEC AI server's public URL is *only* IPv6! By default Docker only gives your container an IPv4 address.

1. Edit `/etc/docker/daemon.json` (with Vim or Nano)
2. After the first curly brace, make a new line and add: `"ipv6": true,` (with the comma because it must be valid JSON)
3. Save and exit
4. Restart the docker daemon: `sudo systemctl restart docker`

---

## Grading

This table shows how many points you get for each segment of the integration.
Each segment is equally weighted.

```{table} Integration Points
| For the ______ segment  | If you...                                                         | You get this percentage for that segment |
|-------------------------|-------------------------------------------------------------------|------------------------------------------|
| Trigger voice recording | Trigger with button                                               | 85% total                                |
| Trigger voice recording | Trigger with Arduino KWS                                          | 100% total                               |
| Voice transcription     | Cold start voice-to-text (model not loaded until trigger)         | 20% total                                |
| Voice transcription     | Warm start voice-to-text (model loaded before trigger)            | 100% total                               |
| Networking              | Send transcription to LLM; LLM extracts and returns the location  | +50%                                     |
| Networking              | GET weather for location from https://wttr.in and print to screen | +50%                                     |
```

# Final Workday

![How neat is that](https://i.giphy.com/CWKcLd53mbw0o.webp)
