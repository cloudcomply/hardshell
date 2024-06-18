# Issue triage

Currently, hardshell uses the issue tracker for bugs, feature requests, proposed style
modifications, and general user support. Each of these issues have to be triaged so they
can be eventually be resolved somehow. This document outlines the triaging process and
also the current guidelines and recommendations.

```{tip}
If you're looking for a way to contribute without submitting patches, this might be
the area for you. 

You can get easily started by reading over this document and then responding to issues.

If you contribute enough and have stayed for a long enough time, you may even be
given Triage permissions!
```

## The basics

hardshell gets a whole bunch of different issues, they range from bug reports to user
support issues. To triage is to identify, organize, and kickstart the issue's journey
through its lifecycle to resolution.

More specifically, to triage an issue means to:

- identify what type and categories the issue falls under
- confirm bugs
- ask questions / for further information if necessary
- link related issues
- provide the first initial feedback / support

Note that triage is typically the first response to an issue, so don't fret if the issue
doesn't make much progress after initial triage. The main goal of triaging to prepare
the issue for future more specific development or discussion, so _eventually_ it will be
resolved.

The lifecycle of a bug report or user support issue typically goes something like this:

1. _the issue is waiting for triage_
2. **identified** - has been marked with a type label and other relevant labels, more
   details or a functional reproduction may be still needed (and therefore should be
   marked with `S: needs repro` or `S: awaiting response`)
3. **confirmed** - the issue can reproduced and necessary details have been provided
4. **discussion** - initial triage has been done and now the general details on how the
   issue should be best resolved are being hashed out
5. **awaiting fix** - no further discussion on the issue is necessary and a resolving PR
   is the next step
6. **closed** - the issue has been resolved, reasons include:
   - the issue couldn't be reproduced
   - the issue has been fixed
   - duplicate of another pre-existing issue or is invalid

For enhancement, documentation, and style issues, the lifecycle looks very similar but
the details are different:

1. _the issue is waiting for triage_
2. **identified** - has been marked with a type label and other relevant labels
3. **discussion** - the merits of the suggested changes are currently being discussed, a
   PR would be acceptable but would be at significant risk of being rejected
4. **accepted & awaiting PR** - it's been determined the suggested changes are OK and a
   PR would be welcomed (`S: accepted`)
5. **closed**: - the issue has been resolved, reasons include:
   - the suggested changes were implemented
   - it was rejected (due to technical concerns, ethos conflicts, etc.)
   - duplicate of a pre-existing issue or is invalid

**Note**: documentation issues don't use the `S: accepted` label currently since they're
less likely to be rejected.

## Labelling

We use labels to organize, track progress, and help effectively divvy up work.

Our labels are divided up into several groups identified by their prefix:

- **T - Type**: the general flavor of issue / PR
- **C - Category**: areas of concerns, ranges from bug types to project maintenance
- **F - Formatting Area**: like C but for formatting specifically
- **S - Status**: what stage of resolution is this issue currently in?
- **R - Resolution**: how / why was the issue / PR resolved?

We also have a few standalone labels:

- **`good first issue`**: issues that are beginner-friendly (and will show up in GitHub
  banners for first-time visitors to the repository)
- **`help wanted`**: complex issues that need and are looking for a fair bit of work as
  to progress (will also show up in various GitHub pages)
- **`skip news`**: for PRs that are trivial and don't need a CHANGELOG entry (and skips
  the CHANGELOG entry check)

```{note}
We do use labels for PRs, in particular the `skip news` label, but we aren't that
rigorous about it. Just follow your judgement on what labels make sense for the
specific PR (if any even make sense).
```

## Projects

For more general and broad goals we use projects to track work. Some may be longterm
projects with no true end (e.g. the "Amazing documentation" project) while others may be
more focused and have a definite end (like the "Getting to beta" project).

```{note}
To modify GitHub Projects you need the [Write repository permission level or higher](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-permission-levels-for-an-organization#repository-access-for-each-permission-level).
```

## Closing issues

Closing an issue signifies the issue has reached the end of its life, so closing issues
should be taken with care. The following is the general recommendation for each type of
issue. Note that these are only guidelines and if your judgement says something else
it's totally cool to go with it instead.

For most issues, closing the issue manually or automatically after a resolving PR is
ideal. For bug reports specifically, if the bug has already been fixed, try to check in
with the issue opener that their specific case has been resolved before closing. Note
that we close issues as soon as they're fixed in the `main` branch. This doesn't
necessarily mean they've been released yet.

Design and enhancement issues should be also closed when it's clear the proposed change
won't be implemented, whether that has been determined after a lot of discussion or just
simply goes against _hardshell_'s ethos. If such an issue turns heated, closing and locking
is acceptable if it's severe enough (although checking in with the core team is probably
a good idea).

User support issues are best closed by the author or when it's clear the issue has been
resolved in some sort of manner.

Duplicates and invalid issues should always be closed since they serve no purpose and
add noise to an already busy issue tracker. Although be careful to make sure it's truly
a duplicate and not just very similar before labelling and closing an issue as
duplicate.

## Common reports


