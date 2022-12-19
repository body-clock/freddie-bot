# Roadmap
 - [x] Break up big functions into smaller functions
   - [x] `download_cat_image`
     - This function does a lot more than the name suggests. We should have separate functions for each of the steps that this function executes.
 - [ ] Refactor code into classes
   - [ ] Lyrics
     - [ ] Get lyrics
     - [ ] Clean lyrics
     - [ ] Select tweet lyrics
   - [ ] Image
     - [ ] Get image URL
     - [ ] Download image into memory
     - [ ] Upload image to s3
     - [ ] Download image from s3 into Lambda /tmp/
     - [ ] Delete image from s3
   - [ ] SongCSV
     - [ ] Download CSV from s3
     - [ ] Turn CSV into list
 - [ ] Set up automatic deployment from GitHub to Lambda
