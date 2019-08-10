# A-Study-on-Eye-Movement-Behaviors-While-Reading-Digital-Learning-Content
The project proposed three eye movement metrics and classification for digital learning slides, attempting to explain the correlation between eye movement bahaviors and degree of interest.

# Analytic Metrics
* FTP - fixation time percentage
* MTTF - mean time to fixation
* SDOF - spatial diversity of fixations
# Project Structure
* calculator - code and output pitures with fixation data 
  + calculator.py - read every single file and output slide info
  + Fixpic - all slides with fixation data
    + A - button mask
    + B - outlier removal
    + AandB - both filter
    + nofilter - original data
  + Outpic - all slides with fixation data mean fixation point
    + red - mean fixation point of original data
    + orange - duration weighted mean fixation point of original data
    + blue - mean fixation point of filtered data
    + deep blue - duration weighted mean fixation point of filtered data
* Pic - all slides pictures
* data - all data here
  + pagecut - calcultaed page switching timing
  + Result
    + Slide table - slide info
    + Lecture table - lecture info
    + Class table - class info
    + Regression - regression analysis
  + ResultPages - calculated slide info
* Outpic - all slides with fixation data mean fixation point
  + red - mean fixation point of original data
  + orange - duration weighted mean fixation point of original data

