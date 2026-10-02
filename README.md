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

## How menu lookup works

Each school's menu system creates a brand-new, opaque menu ID every month. Rather than hardcoding a monthly ID (which would need manual updates every month), `index.html` stores a stable `menuTypeId` per school and automatically looks up the correct month's menu ID at runtime via the school nutrition site's `menutypeController.php/show` endpoint. No manual updates should be needed month to month.

### If a school switches to a new menu system (rare)

If menus stop loading entirely and the school has set up a brand-new menu type (not just a new month), you'll need to find the new `menuTypeId`:

1. Open the full menu link for that school on the school nutrition site.
2. Note the menu `id` from the URL (after "id=").
3. Fetch `https://www.schoolnutritionandfitness.com/webmenus2/api/menuController.php/open?id=<that id>` and read the `menu_type` field — that's the new `menuTypeId`.
4. Update the corresponding entry in the `SCHOOLS` object in `index.html`.