#; last modified by: TianXie  in: Oct 19, 2018
#[confidential]
apikey='YOUR API KEY'

#[bounding]
bounding = {
  'south':42.328166,
  'west':-83.056673,
  'north':42.332751,
  'east':-83.053417
}
#[searchingParameter]


#;Warning: change searching radius may led to extra API usage or incomplete data
#;Because of the limited response by Google API(60 for each requests), you want
#;to make sure the output record doesn't exceed that limit
searchingParameter = {
  'searchingRadius':300,
  'type':'store'
}

#specify the type of the place you want to scrape
#to see available type option,
#please visit: https://developers.google.com/places/supported_types

#[output]

outputFolder='output'
