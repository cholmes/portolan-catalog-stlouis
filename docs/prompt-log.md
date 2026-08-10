# Prompt log — St. Louis open data mirror

Every instruction given in this project, verbatim and in order, reconstructed from the
session transcript. It covers the two repos built here — `portolan-catalog-stlouis`
(the STAC catalog published to Source Cooperative) and `stlouis-data-browser` (the
portolan-browser fork) — plus the upstream fixes they prompted in `portolan-browser`
itself.

**43 prompts**, from Aug 4, 22:27 UTC to Aug 10, 11:47 UTC.

A few conventions:

- Text is unedited, typos and all. `[Image #N]` marks a screenshot that was pasted
  inline — the images themselves are not in the transcript, only their position.
- **(queued)** marks a prompt typed while a previous one was still running. Roughly
  half of them are; the pattern here was to keep reviewing while work was in flight
  rather than wait for each turn to finish.
- Slash commands (`/model`, `/compact`), interrupt markers, and background-task
  notifications are omitted. They are not instructions.

---

## Kickoff — scope and ground rules

*The whole project brief, delivered in four messages over half an hour.*

**1. Aug 4, 22:27 UTC**

> can you make a pair of repositories that follow /Users/cholmes/repos/trimet-data-browser and /Users/cholmes/repos/portolan-catalog-trimet (and also ~/repos/portolan-nl-catalog and ~/repos/ftw-data-catalog) that portolan-ify https://www.stlouis-mo.gov/data/ - st. louis open data? use your portolan bootstrap skill and check the latest in the spec in ~/repos/portolan-spec - you can assume https://github.com/portolan-sdi/portolan-spec/pull/97 will be merged. Let's start with a top 20 most interseting data sets from st. louis, and lets make the result look / feel as similar to what they have as possible.

**2. Aug 4, 22:27 UTC** *(queued)*

> and create a second plan to execute on getting all geo related (and geo adjacent, like joinable) data into it.

**3. Aug 4, 22:56 UTC** *(queued)*

> Oh, also assume https://github.com/portolan-sdi/portolan-spec/pull/124 is in - use the table stac extension for all

**4. Aug 4, 22:58 UTC** *(queued)*

> Oh, and do at least 3 styles for all data, 5 if warranted - do deep examination of the data and pull out interesting stuff to highlight, and make sure each has a legend - check the other repos for how to make sure a legend appears.

---

## First review — data cleanup, styling, and the shape of the catalog

*The first look at a working catalog. Mostly screenshots with corrections attached.*

**5. Aug 5, 04:24 UTC**

> [Image #1] let's get the bbox around the 311 data a bit tighter. Remove/fix outliers that aren't in the bounds of st louis.

**6. Aug 5, 04:26 UTC**

> oh, looks like you have lat / lon still in as columns[Image #2] - lets just take those out.

**7. Aug 5, 04:26 UTC** *(queued)*

> [Image #3] also this description - let's make that a real markdown link

**8. Aug 5, 04:27 UTC** *(queued)*

> [Image #4] also this 'tiles' button doesn't show up till you click on it, and one of the other asc/desc buttons also seemed to have an issue.

**9. Aug 5, 04:34 UTC**

> [Image #5] also these two look the same, and not great. can you do a nicer style where each is a different color, or at least repeating sets of colors? And you can do some with labels of the names of things? Also the top [Image #6] looks boilerplate-y. [Image #7] can we have it look more like this? [Image #8] acn we replicate their 'topics' and tag with those and let people browse by those? How many more datasets are there that we could add? [Image #9] is also nice. [Image #10] and are we reusing their tags?

**10. Aug 5, 04:36 UTC** *(queued)*

> Hmmm... it is not that many total datasets: https://www.stlouis-mo.gov/data/datasets/index.cfm - having all those topics seems overkill as they likely aren't all used. Could you consolidate to the main topics and just have those? But have the home page / landing page display topics and let you click to filter.

**11. Aug 5, 04:39 UTC** *(queued)*

> And can you also scan https://stlcity.maps.arcgis.com/home/gallery.html?sortField=relevance&sortOrder=desc&mode=keyword&focus=layers and give me an assessment if there's anything that's actually interesting / valuable there that we should extract and expose? I see a bunch of not so great stuff, and duplicates of what we have, but if we can surface some actually interesting / valuable data that'd be nice.

**12. Aug 5, 04:40 UTC** *(queued)*

> is there any reason you're preferring gdal/ogr over gpio / geoparquet.io? If there's nothing blocking can you shift the scripts to do that?

**13. Aug 5, 04:41 UTC** *(queued)*

> Biking Infrastructure Map_WFL1 does look cool, let's get bike infrastructure in if it's not already.

**14. Aug 5, 04:49 UTC** *(queued)*

> can you push / publish soon? Before I hit session limit.

**15. Aug 5, 04:49 UTC** *(queued)*

> can defer the conversion to gpio

---

## Thumbnails and tiling performance

*The parcels layer kept crashing Chrome. This phase is almost entirely about tile size.*

**16. Aug 5, 14:15 UTC**

> continue

**17. Aug 5, 14:40 UTC**

> [Image #11] also some of the thumbnails don't seem to fully be there. Like this one. [Image #12] [Image #13] [Image #14] [Image #15] [Image #16]. They also all run together a bit with all having the same shape. Could you have a few of them be zoomed in? Some in to real detail, some just getting to fill the box, like an overview but not the long rectangle.[Image #17] would be an example - get most of it. The boundaries / bborders should probably be full, but things that are subsets can be zoomed in. Can use your discretion overall, but n[Image #18] with city blocks is one that is nicer zoomed in (though let's get a default rendering that helps you visualize each block more - that one is 'city render' which is ok, but default (city blocks) that is semi transparent with a good 'block' color and a label with name? and then for the alternate styles let's color by ward, precient, ward, census block - let people see what block things are in, the tinted blokcs is not good, can barely be seen. n[Image #19] also both these look good, but can you have them not be the same? Make one bolder, with a bit of a different color palette. Also on parcels https://cholmes.github.io/stlouis-data-browser/#/parcels/collection.json I got 'waiting' on chrome it got laggy and then basically crashed - 7 gig of memory - seems to happen when I zoom in. and tax-abated parcels seems to behave similarly. [Image #21]. [Image #22] - looks like  the first pmtiles load is 11mb? That's way too big, should use the 500kb max per tile and use tippecanoe's thinning better. What wass the command you used to create those?

**18. Aug 5, 15:38 UTC**

> [Image #23] can  you make the parcel thumbnail more zoomed in, so that there aren't thinned parcels. And TFI [Image #24] more zoomed in, so it covers the full card / aspect ratio. And actually more generally can you match the aspect ratio of all the more zoomed in thumbnails to match the cards they appear in? They're still [Image #25] long. And I'm still getting hangs on the parcels data - out of memory from chrome after looking at it for awhile / trying to move. On https://browser.portolan-sdi.org/#/external/data.source.coop/tge-labs/st-louis-open-data-mirror/parcels/collection.json I was able to zoom in a bit and then zoomed out and it started hanging / slowing. on https://cholmes.github.io/stlouis-data-browser/#/parcels/collection.json?.asset=asset-parcels-tiles I got less far [Image #26] also I think a hard 500kb cap isn't working - now at high zoom levels there's not full parcels. Can you ensure that at zoom level 14 all the data is there?

**19. Aug 5, 16:47 UTC**

> have you pulled in all the data that makes sense yet? Like additional layers from st louis open data portal and arcgis online?

**20. Aug 5, 17:08 UTC**

> There should be a way to sort with gpio - you can just do a specific sort call if you can't embed it in the parquet -> parquet convert

**21. Aug 5, 17:14 UTC**

> parcels is better, but I'm now getting a hang when I switch to assessed value legend

**22. Aug 5, 17:20 UTC**

> can we fix that style switching swap upstream in portolan-browser - so it always uses pmtiles if it's there and switches without reloads?

---

## Joins, and the rest of the data

*Deciding how tabular datasets reach the map, then expanding to the full ingestion plan.*

**23. Aug 5, 17:39 UTC**

> Ok, let's do the next set of data. But let's tweak how we do the joins - can we make it so there's a  PMTiles with the geometries for each of them? Like do the actual join for the PMTiles for people to see it. ANd then in the agents.md explain exactly to agents how to do the join to get a .parquet, or a geopackage / shapefile. But we'll keep it as a non-geoparquet on the portal.

**24. Aug 5, 18:53 UTC** *(queued)*

> Go for the next ones, all the way through sub catalog re org.

---

## Deeper insight, documentation, and the topic reorganization

*The turn from 'does it work' to 'does it say anything'.*

**25. Aug 5, 20:51 UTC**

> great! [Image #27] parcels '2020 fabric' doesn't seem to show anything. What is this 'fabric' term you're using through out? I don't understand, and don't think others will... Could we get some landuse and zoning visualizations on that? In general can you inspect the data and upgrade the styles so they give deeper data insights? on this and other tabular data stuff. One little idea - on parcel sales show the sale price vs area - like calculate the cost per square foot. Also for 'quick stats' - it just says the number of collections. Let's show total number of datasets, total number of features mapped, total amount of data. Also let's upgrade our readme's / descriptions / agent.md's Review https://github.com/portolan-sdi/portolan-spec/blob/main/specs/best-practices/documentation.md and https://github.com/portolan-sdi/portolan-spec/blob/main/specs/best-practices/grader.md along with https://github.com/portolan-sdi/portolan-spec/blob/main/specs/best-practices/philosophy.md and see the agent files in https://browser.portolan-sdi.org/#/external/data.source.coop/cholmes/portolan-nl/catalog.json?.language=en and https://github.com/portolan-sdi/portolan-spec/tree/main/examples/catalog/portolan-reference  And include lots of markdown links in the text, and when you do that do the link to source.coop instead of data.source.coop so that things render. And is there more you can put in the descriptions of the columns? Deeper research on what those mean? [Image #28] like pipe material - these numbers don't mean much. Generally try to research and surface what different columns mean.

**26. Aug 5, 21:00 UTC** *(queued)*

> [Image #29] [Image #30] - it looks like the esri imagery layer ends up overlaid on top of the data layer? light and dark work fine.

**27. Aug 5, 21:02 UTC** *(queued)*

> [Image #31] (this can be after) - can we redo the core catalogs to use the 'topic' just like in the main site? And also get those icons for each to display next to them.

**28. Aug 5, 21:04 UTC** *(queued)*

> WIth that restructure I do think we want to be clear about what department things are from. Should perhaps make a clear 'tag' for each so it's easy to see all from one department.

**29. Aug 5, 21:20 UTC**

> [Image #32] let's put this below the catalogs [Image #33] and have this combine with [Image #34] - get the fuller descriptions and icons to actually be on the cards you can click on. Like lead with the actual browser - the topic interaction isn't great. I just wanted the icons on the catalogs

**30. Aug 5, 21:21 UTC**

> [Image #35] and can we do 'browse' button in the same color as this, with [Image #36] this for mouse over, like the st. louis site?

**31. Aug 5, 21:41 UTC**

> [Image #37] let's call them 'datasets' instead of collections. And 'rows' instead of 'features'. And don't put the map styles, but put the number of departments there that are represented with data here.

---

## Browser polish

*Home page layout, city-matched buttons and icons, and one broken deploy.*

**32. Aug 5, 22:04 UTC** *(queued)*

> I tried to push the browser changes but I think it borked something ont he live site. Please fix that, and also get out the new descriptions in the data catalog

**33. Aug 5, 22:07 UTC** *(queued)*

> Oh, can we use the exact icons from: https://www.stlouis-mo.gov/data/  ?[Image #38]

**34. Aug 5, 22:09 UTC**

> (and things look fine now, thanks)

**35. Aug 5, 22:10 UTC** *(queued)*

> [Image #39] the browse is a bit weird, seems like a full line vs just a button? I don't think we need the 'cloud-native mirror' across the top, could just have the browse thereas a blue/red button.

**36. Aug 5, 22:13 UTC** *(queued)*

> [Image #40] zip code styles seem off. First one has a legend of a bunch of colors, but only one color shows. [Image #41] city render is blank, and subtle tint looks blank too. Should do one with labels so you can see the zip codes.

**37. Aug 5, 22:14 UTC** *(queued)*

> whats the status of improved column descriptions? I don't see them in the stac table metadata. [Image #42] also this file a service request isn't a real link - can  you make sure anything in a stac description / readme gets markdown link treatment? So it becomes clickable.

**38. Aug 5, 22:34 UTC**

> go for it

**39. Aug 5, 22:40 UTC** *(queued)*

> [Image #43] let's put these above the catalogs (but keep 'data by tag' below) on the home page.

---

## Provenance and the AI demo

*Linking the city's own files as assets, and thinking about what the catalog can answer.*

**40. Aug 6, 03:09 UTC** *(queued)*

> Could you include as much of the source files as possible? Like if there's geojson and shapefiles include them as assets, directly linked to their original locations. If it's a feature service / wfs then include the link and describe what was done to get the data.

**41. Aug 6, 03:30 UTC** *(queued)*

> I'm looking to do a demo of using ai to 'chat' with the data. What do you think are some of the more interesting questions about st. louis that you might be able to answer using this set of data? Especially insightful things, non-obvious things, and things that are the result of joins of more than one dataset.

---

## Publishing

*Shipping it, and writing this.*

**42. Aug 6, 23:28 UTC**

> can you commit and publish?

**43. Aug 10, 11:47 UTC**

> can you make me a doc of all the prompts I've used in this project?

---

## What the shape of this log shows

Almost nothing here is a specification. The opening prompt sets the goal and the
constraints; everything after it is a reaction to something visible on screen — a
thumbnail that reads as a smear, a legend with one color, a browser tab eating seven
gigabytes. Eighteen of the 43 prompts carry screenshots — 42 images in all.

Three threads run the length of the project:

- **Match the city.** Their topics, their icons, their button colors, their words
  ('datasets' not 'collections', 'rows' not 'features').
- **Make the data say something.** Repeated pushes past a working map toward styles,
  column descriptions, and derived measures like cost per square foot that carry an
  actual finding.
- **Fix it upstream.** When the style switcher reloaded tiles unnecessarily, the
  instruction was to fix `portolan-browser`, not to work around it here.

