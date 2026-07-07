# ziyun-z.github.io

My personal website and blog, built on the [Clarity](https://shikun.io/projects/clarity) template.

## Structure

- `index.html` — homepage (intro + blog list)
- `gallery.html` — photo gallery (masonry grid + lightbox)
- `blog/` — one HTML file per post; `blog/post-template.html` is the starting point for new posts
- `gallery/` — image files shown in the gallery
- `assets/`, `clarity/` — template styles, fonts, icons, and scripts (`assets/stylesheets/custom.css` holds site-specific styles)

## Add a blog post

1. Copy `blog/post-template.html` to `blog/your-post.html` and write it.
2. Add a matching `<a class="post-card">` entry to the blog list in `index.html` (newest on top).

## Add a gallery photo

1. Drop the image into `gallery/`.
2. Copy a `<figure>` block in `gallery.html` and update its `src` and caption.

## Preview locally

```
python3 -m http.server 4599
```

Then open http://localhost:4599/. (Serving from the project root matters — the blog pages link to shared styles one level up.)
