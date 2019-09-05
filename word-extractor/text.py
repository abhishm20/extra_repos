import rake
import operator

rake_object = rake.Rake("SmartStoplist.txt")

sample_file = open("./text1.txt", 'r')
text = sample_file.read()
keywords = rake_object.run(text)
print "Keywords:", keywords
print "count:", len(keywords)