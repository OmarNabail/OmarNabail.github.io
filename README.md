# Omar Nabail — Portfolio

Source for [omarnabail.github.io](https://omarnabail.github.io), an evidence-led portfolio covering AI systems, model evaluation, deployment, and software engineering.

## Edit the portfolio

- Edit text, project descriptions, links, and metadata in `build.py`.
- Edit colors, spacing, typography, and responsive layout in `dist/styles.css`.
- Replace `assets/Omar-Nabail-CV.pdf` when the CV changes.

### Edit directly on GitHub

Open the file, select the pencil icon, make the change, and commit it to `main`. GitHub Actions automatically runs `build.py`, validates the result, and deploys the generated `dist/` website.

Do not edit the generated HTML files in `dist/` for content changes; `build.py` will replace them during deployment.

### Edit locally

```powershell
python build.py
python check.py
git add build.py check.py assets dist
git commit -m "Describe the portfolio change"
git push origin main
```

Every push to `main` regenerates and deploys the website through GitHub Pages.
