# KOR MEET Landing Page

Static landing page for KOR MEET. This project does not need a build step or package install. You can preview it locally with a simple HTTP server.

## Local Preview

Start the preview server from the project root:

```bash
cd /Users/tjaypark/korcall-landing
python3 -m http.server 18091
```

Open:

```text
http://127.0.0.1:18091/
```

## Stop The Server

Find the running server process:

```bash
ps -ax | rg 'http.server 18091'
```

Stop it with the PID from the first column:

```bash
kill <PID>
```

## Notes

- Main page file: `index.html`
- Assets live in `assets/images/`
- This is a plain static site, so edits are reflected after a browser refresh
- If `18091` is already in use, start the server on another port such as `18092`

```bash
python3 -m http.server 18092
```
