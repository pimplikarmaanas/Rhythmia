# RunIt

## Inspiration and What it does
Athletes looking to progress in their careers or any person looking to get healthier often listen to music during their exercise sessions. We have noticed that a common problem among those who work out is that when going at high intensity, the music doesn't match up with their pace. For example, picture a runner listening to music as he is running up a hill. He decides to push faster toward the uphill portion of his run. His music, however, is not matching this, setting off his entire rhythm and creating difficulty in his workout. Rhythmia poses a solution to this problem. Rather than you having to match the pace of your music, the music matches your pace!  The application determines the intensity at which you are exercising using your heart rate provided by any fitness accessory. Using this, it recommends a song from YOUR Spotify account! That way, a person no longer has to curate different playlists for each of their workouts, but rather the music follows you along. In addition, Rhythmia mixes things up by also recommending songs from public Spotify playlists based on songs that you already like. This gives you a good mix of familiar and unheard songs on your workout that matches your intensity. 


## How we built it
In order to build this we used Tkinter for our UI, Sklearn for our Knn model used to recommend songs, and the Spotify API to gather private user song data in order to recommend and provide users with songs in their Spotify queue. 
## Challenges we ran into

The major challenge we ran into was the integration of the AI model with the rest of our program. While the AI model recommended songs on its own, when we tried to integrate it with the application, it started to have issues with the way it is being trained.  Furthermore, Spotify does not have an empty_queue function, so we had to work around this when dealing with a user's Spotify queue.

## Accomplishments that we're proud of
We are proud of how well we communicated and worked together. We are also proud of how well we executed an original idea we had for our first hackathon!

## What we learned
Overall, we learned to integrate an AI model with continuous API calls.  Along with this, we learned to work as a team and split up parts of the project accordingly so that we can be the most productive and have the most fun!

## What's next for Rhythmia

In the future, Rhythmia is looking to use either FitBit or AppleHealth API to allow users to have a fully functional interface while they are running. This will be in the form of an Apple application and/or a WatchOS app. Furthermore, we look to add another mode called "Program" where a user can set their target and minimum BPM and they can work up to that BPM and slow down if they need to. 
