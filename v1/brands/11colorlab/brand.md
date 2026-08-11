# colorlab.rj11.io

Temporary testing brand for exhaustive Tailwind color previews. The config is a
stable rendering baseline; the sweep tool varies the signal and renders both
the dark and light family contexts without changing this file.

## Palette decision

Mode dark baseline. Signal `#F97316` on ground `#0A0A0A`: **7.06:1**.

The baseline signal is only a valid initializer. The experiment covers every
Tailwind v4.3.2 default token, including colors below the normal 3:1 graphic
floor. Contrast is recorded for selection, never used to filter the sweep.

<Why this colour. What it was chosen against — name the candidates that lost and
the number that killed each one. A non-text graphic needs 3:1 against its own
ground; aim past it. A neutral signal (silver, grey) also needs checking against
the ink and the footer grey, because it has no hue to separate it.>

## Notes

The sweep source is `v1/scripts/data/tailwind-v4.3.2.css`, derived from the
Tailwind default theme and documented at https://tailwindcss.com/docs/colors.
The preview tool converts the source OKLCH values to clamped sRGB hex because
brand configs use six-digit hex values. This brand is not a production brand.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
