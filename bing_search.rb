#!/usr/bin/env ruby
require 'searchbing'
require 'yaml'
require 'json'

#Example usage
# $ruby bing_search.rb "query" number_of_results

creds = YAML.load_file('creds.yaml')
web = Bing.new(creds['bing']['key'],ARGV[1].to_i,'Web')
response = web.search(ARGV[0])
puts response.to_json
