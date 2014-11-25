task :setup do
  `pip3 install -r requirements.txt || pip install -r requirements.txt`
  `bundle install`
end

task :clean do
  `rm -f queries/*`
end
