# School Lunch Menu

A simple single-page web app that displays the current school lunch menu, pulled live from the School Nutrition and Fitness API.

## Features

- Today's menu and full week view
- Allergen info displayed per item
- Built with plain HTML, CSS, and JavaScript — no dependencies

## Usage

Open `index.html` in a browser. No build step or server required.

## Notes

Allergen information is sourced automatically and is not confirmed or monitored by a person. This site was built with AI assistance and may contain inaccuracies.

## Yearly update instructions

If the menu isn't loading correctly (typically at the start of a new school year), you'll need to replace the menu IDs in the index.html file.

1. Get the new menu ID from the school nutrition site URL — it's the value after "id=".
2. Open index.html and replace the old ID on lines 136 and 122 with the new one

This tells the page which menu to fetch from the school's system — it needs to be updated each school year when the school creates a new menu record.