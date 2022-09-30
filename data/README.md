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


`new_json_file_with_lap_times.json`

- This file contains the full dataset.
- It contains the most recent lap times of each car
- Rather than using the full dict like structure with key value pairs, we are using 
a List/array. This is to reduce the size of the file. We can do this as we have know 
the order of the keys, and their order/ position doesn't change throughout (the amount 
of cars is always the same, and the keys are always the same).
- It is a list of lists, and at the end of each nested list, is the timestamp... (we 
write "timestamp" before it to be clear, but it can easily be accessed by `[-1]` or similar)

`very_short_new_json_file_with_lap_times.json`

- Same as the above, but a shorter version of it. 
