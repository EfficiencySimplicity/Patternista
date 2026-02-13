# 2/13/2025

PatternMatcher needs an uncertainty feature in its patterns. Basically an alpha channel, where the color difference
doesn't really matter that much, so no weight on the average in that area, most of it concentrated on the main
feature of that pattern. Something to say, "I'm just looking for an eye, I don't care about the fur color around it",
or, "I'm just looking for the nametag on the collar, I don't care about the color of the collar", or, "I'm looking for
a person, I don't care where that person is". And basically you get this uncertainty channel by looking at what makes
you uncertain. You'd have a pattern looking for stop signs, and it would be given stop signs, and the center would mostly
look the same as always, a stop sign, but the outside would have lots of different surroundings, and so keeping those features
would lead to that tannish blurry mess you get. And so you'd have uncertainty in those areas, essentially an error bar telling
how far you've seen that area deviate from it's stated values.

PatternMatcher also needs the ability to supply other functions than the comparison one, namely a modification one, where you get
the pattern, the sample, the difference, and the learning rate? / number of examples seen, and return the new pattern. This might help
in the case of pitting 2 PatternMatchers against each other, and trying to keep their features separate. And maybe some other variable
functions could be implemented.

Also, for the reconstruction of filters (what sets PatternMatcher apart from normal CNNs) you should set a threshold, basically say, 
"Average the multiplied-by-filter-value patterns only above this margin", 'cause of course filters store their expected values for every
pattern under them, and some expecting a .5 activation value, for instance, you can't reconstruct it exactly, and the results get a little messy.
Just imagine a stop sign pattern, and a slider that you slide it, and a sort of vector-graphics-y stop sign appears, transparent in the edges
(ooh, object isolator?!) and the more you move the slider, the more details it gets, until it gets a bit messy, then you stop. Although maybe
the messiness will not happen that much if the uncertainty is implemented, 'cause the non-active patterns will be close to 0 if they didn't find
what they're looking for. Yeah, uncertainty behooves patterns to target things narrowly, and so the values will be closer to 0 or 1 most of the time.