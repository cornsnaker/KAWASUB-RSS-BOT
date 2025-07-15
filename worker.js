addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const { searchParams } = new URL(request.url);
  const url = searchParams.get("url");

  if (!url || !url.includes("terabox.com/s/")) {
    return new Response(JSON.stringify({ error: "Invalid TeraBox URL" }), { status: 400 });
  }

  try {
    const page = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0",
      },
    });
    const html = await page.text();

    const match = html.match(/"downloadUrl":"(https:[^"]+)"/);

    if (!match) {
      return new Response(JSON.stringify({ error: "Download link not found or file is private" }), { status: 404 });
    }

    const downloadUrl = decodeURIComponent(match[1].replace(/\\u002F/g, "/"));

    return new Response(JSON.stringify({
      status: "success",
      download_url: downloadUrl
    }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
}
