**This is a file for describing each of our `.json` files given
that we have many and need to keep track...**

I will list the ones that are important 

---

### Files 

`stream_data_short_keys.json`

- This file contains the full dataset (all timestamps)
- This contains short keys (e.g. `t` instead of `throttle`)
- This file also contains constant timestamps every 0.5 seconds 

`very_short_stream_data_short_keys.json`

- Same as above, except that it only contains a portion of the full 
dataset -> going from the 1993rd second to 2067th. 

`stream_data_with_lap_times.json`

- This file contains the full dataset 
- It also contains the `"mostRecentLapTime"` key for each car!

`very_short_stream_data_with_lap_times.json`
- This file is the same as the above, except it's a shorter version 
- Note that "mostRecentLapTime" is always 999 as it's the first lap
