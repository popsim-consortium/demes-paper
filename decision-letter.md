GENETICS-2022-305343

Demes: a standard format for demographic models

Dear Dr. Kelleher:

Two experts in the field have reviewed your manuscript, and I have read it as
well. I am pleased to inform you that, with minor revisions, it is potentially
suitable for publication in GENETICS. The reviewers have comments and concerns
that need to be addressed in a revised manuscript. You can read their reviews
at the end of this email.

Demes is an important advance to standardizing the implementation of popgen
models, and so a very welcome contribution. The reviewers give a number of very
useful suggestions. I leave it up to you how you proceed with incorporating
changes based on these comments, as you will have more of a sense of how the
comments overlap those from other users, but please do write a response to all
of the comments.

--------------------------------------------------------------------

# Reviewer #2 (Comments for the Authors (Required)):

This manuscript presents the Demes data model and related libraries ecosystem.
I have been using it for some time and was happy to review the paper as I find
it really useful, intuitive and well designed (as are a lot of tools developed
by those authors and the whole community of the popsim consortium and tskit).
The main usage I have for it at the moment was to switch effortlessly between
msprime and SLiM using the same demographic model, loved that. But as described
in the paper, it has a lot of other qualities. Overall, this format is a really
useful addition to the field and which I hope will be largely adopted.

I don't have much to add to this manuscript other than a few comments that I
hope will help answer a few questions that other readers could have. My main
comment below is that an example of the YAML format should be included in the
main text.


## Comments

- I usually like when there is a link to the software directly in the abstract
  in those kind of papers, it avoids scrolling through it as links are
sometimes in different places in those type of manuscripts.

- I suggest including the example of the YAML format in the main text.
This is too sad that the center piece of this paper has been relegated to the appendix :(
Show us how easy it is to understand the model from the YAML format!
Maybe FigA2 is a bit too long, but FigA1 A and B could work well.

- A fair question that could be asked by any potential user could be: Are there
  versions to this data format? There is no version argument in the YAML file,
what if the format changes in the future? How would my model format would be
recognized by the parser? I get that it is designed with stability in mind and
it is done well, but we've seen formats change for other things through time
(e.g. in bioinformatics) to adapt to new usage.

- There might be the need to specify how the initialization time of the whole
  model is dealt with. This is kind of straightforward when thinking about
coalescent models for people used to it. But not for forward-time simulations.
Especially that in your examples there are no start_time for the first
population. This might be hard for some users to wrap their head around.

- p2 you discuss the defaults of CLI and input parameter formats but not of
  APIs. It could be said that APIs require some learning (of both the interface
and the given programming language for users not used to it). Learning a new
API each time you change simulator is also time consuming.

- p2 "YAML format" you could specify that it is a data serialization language

- p12 "time units is in generations" you could precise it is the default value here, if it is?

- p12 "such as years, accompanied by the generation time". Might be worth
  detailing that it is needed as simulators work with generations and not
years, so there needs to be some kind of conversion.

- p12 "function defined by start and end sizes" You should detail here what are
  the models of population expansion available and what is the default. Linear,
exponential, etc.?

- p12 "S are born via [...]" missing that S is a proportion

- p13-14 "Other implicit values [...]" until end of paragraph, this part with
  the example could be worth integrating into the main text as this is a major
thing to understand about the data model in my opinion.

- Section A3: you could also detail that having common parsers allows for
  consistent and informative error messages when it comes to missing values or
issues in formatting.

- p15 what's the difference between "genome annotations" and "sequence annotations"?


## Random thoughts I had while reading the paper, to discuss (or not)

- I wondered if such format couldn't be used as a way to increase (spoken)
  language inclusivity. I guess it would be fairly easy to have dictionaries
including multiple translations for each keyword of the format in the parser.
That way you could write your model in Japanese or Spanish and it could still
be read without issue.

- Do you think such plain text format also provide a better substrate for
  versionning demographic models? Could be mentioned.

--------------------------------------------------------------------

# Reviewer #3 (Comments for the Authors (Required)):

In their paper entitled "Demes: a standard format for demographic models",
Gower et al. propose a new way to describe (historical) demographic models of
populations.

The aim of Demes is to provide a standardized way to describe demographic
models to be used by various programs performing genetic simulations, which
currently have different ways to specify the simulated demography. The
intention is to facilitate information exchange and avoid translation problems
when passing from say a simulation software to a parameter estimation program,
if both would use the same input file to describe a demographic model.

The Demes data model is implemented in a text file using the YAML serialization
language, which is often used for configuration files or bioinformatics
pipeline descriptions. YAML uses a convenient human-readable syntax, that is
relatively intuitive to read. Two formats are proposed: a Human data Model
(HDM) supposedly easy to read by human users, and a more elaborate Machine Data
Model (MDM) used for processing. A parser (implemented as Python or C
libraries) is provided to translate HDM into MDM. Overall, I find this
initiative highly welcome as it makes a lot of sense to have the same input
file that could be used by several programs. One could thus use a given
demography inferred from neutral markers (e.g. dadi) to specify a model using
selection implemented using a forward in time simulator (e.g. slim). This is
possible since the specification of demography is separated from the
specification of the genetic model (selection, mutation, recombination).

I have found the paper clearly written and I have just a few comments,
regarding the structure of the paper and the Demes implementation itself.

I have two major concerns. The first one is about the two formats: HDM and MDM.
Contrary to what the author say, I have found the HDM more confusing to read
than the MDM, which is much more explicit (see minor comments below). My
impression is that naive users would more easily create mis-specified models in
HDM than MDM, as HDM is using a lot of implicit definitions (to avoid
redundancy). My relative extensive exposure to the feedback of users reporting
bugs for my own software tells me that users do not carefully check the
structure of their demographic models, and explicit definitions help them in
making it right. Related to that, it is unclear if the default format should
always be the HDM, which would each time need to be parsed into MDM or if
programs could use the MDM as the default input file format. Having both
possibilities would be great, but personally I would just remove the HDM
format, and add some of its nice features to the MDM (e.g. defaults)

The second concern is about the use of a backward-in-time timescale (zero =
present) with a forward in time definition of epochs. It leads to strange
definitions, like a start time set to infinity (as in Fig. A1C), which will be
difficult to implement in forward in time simulators, as they always need to
define a burn-in time. I thus found quite confusing that a start_time is always
larger than an end_time. It would make more sense to use a backward approach
for both the time definition and the demographic definition of epochs (maybe
begin with the more recent epochs and finish with the more ancient ones).

## Minor comments:

- p. 12 Population dynamics. I am not sure that it is necessary to assume a
  specific population dynamics model (e.g. Wright-Fisher model) for a data
format. Similarly, it is not necessary to define how allele frequencies would
change in the population upon selection. Some simulators will implement
selection differently (viability selection, fecundity selection, and selection
could be implemented before or after migration) and, again, this does not
belong to a demography specifying data format. I understand that the authors
wanted to distinguish soft from hard selection, where population size might
depend on average fitness in the latter mode, but there ae so many ways to
implement selection that it should be left to the specific programs reading the
demography.

- p. 12 selfing and cloning. These two parameters are making more sense for
  forward than backward simulators, and they thus do not seem to be fully
generic.

- p. 13: Defaults and inheritance. It is not entirely clear to me what happens
  when a default parameter is superseded in a given ancestral population. Is
the new value inherited in the daughter populations or is it the default value
that applies?

- p. 14. Parsers. It is a good idea to provide HDM to MDM parsers, but I note
  that each program reading an MDM will also implement its own parser to read
it and translate it to program specific parameters. Again, it would make more
sense to me to have a single format and no parser. Rather some parser making
sure that the demographic model makes sense could be useful: i.e. checking that
population ancestors have all been defined, or that end_times are compatible
with start_time.

- p. 16: migration section might become hard to read when there are more than a
  few migration rates to specify. A migration matrix representation would make
more sense, or a way to simplify notation, by perhaps specifying some template
for the parameters identifiers and only specify the values: Template: {source,
dest, start_time, end_time, rate} And then just entering values: { X, Y, 100,
0, 50, 0.0001}

- p. 17 : Whole HDM model is looking strange for a naive user, with a lot of
  implicit parameters probably set at default values. For instance

- is start time infinity by default for ancestral population?

- AFR and EUR have no starting times, which suggests that they are created when
  their ancestral population ends. But what if AFR and EUR were branching off
ANC at different times?

- migrations section looks strangely defined. Is symmetric migration
  implemented by default? Starting time is not specified for first epoch. Does
it mean the epoch starts with the creation of AFR and EUR? But again what if
AFR and EUR would have been created at different times?

- It is good to have a standard way of specifying a given demographic scenario,
  but it would also be good to have a standard way to specify genetic data to
be simulated, and to link it to the demography.

- Finally, I see the point of separating a model from the sampling, but in some
  cases it could be beneficial to mention them in the same file, for instance
if you would like to simulate data at different time points from the same
population. Making sample size part of the properties of a deme would make it
more efficient than specifying it from outside.

Laurent Excoffier
