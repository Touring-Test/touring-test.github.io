---
title: ""
layout: default
---
## Totals
{% assign total_miles = 0 %}
{% assign total_hours = 0 %}
{% assign total_tours = 0 %}
{% for post in site.posts %}
  {% assign total_miles = total_miles | plus: post.distance_traveld_NM %}
  {% assign total_hours = total_hours | plus: post.duration_h %}
  {% assign total_tours = total_tours | plus: 1 %}
{% endfor %}

| ---            | --:                          | --              |
| total distance | {{ total_miles }}            | nautical miles  |
| total time     | {{ total_hours | round: 0 }} | hours           |
| total #        | {{ total_tours }}            | logbook entries |

## Passage Index

|Date|from|via|to |dist (NM)|time (hours)|avg speed (kn)|Crew|Skipper|Vessel|hyper- links|
|--- |--- |---|---| --:     | --:        | --:          |--- |---    |---   |---         |{%
 for post in site.posts %}
| [{{ post.date | date: "%Y-%m-%d" }}]({{ post.url | relative_url }}) | {{
 post.origin_locn         }} | {{ 
 post.via                 }} | {{ 
 post.terminus_locn       }} | {{ 
 post.distance_traveld_NM }} | {{ 
 post.duration_h          }} | {{ 
 post.distance_traveld_NM | times: 1.0 | divided_by: post.duration_h | round: 1 }} | {%
 if post.crew %}{{ post.crew }}{% else %}*solo*{% endif  %} | {{
 post.skipper             }} | {{
 post.tags[0] | split: '_' | last }} | {%
 if post.gps_track %} [track]({{  post.gps_track | relative_url }}) {%
 endif %}{%
 if post.photos    %} [photos]({{ post.photos    | relative_url }}) {%
 endif %} | {%
 endfor %}
