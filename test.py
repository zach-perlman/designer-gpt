import base64

# Example HTML string
html_string = """
        <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube Home</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">

<header class="bg-white shadow p-4 flex justify-between items-center">
    <div class="flex items-center space-x-4">
    <img src="/path/to/logo.png" alt="YouTube Logo" class="h-8">
    <div class="flex items-center bg-gray-200 rounded overflow-hidden">
        <input type="search" placeholder="Search" class="px-4 py-2">
        <button class="bg-red-500 px-4 text-white">Search</button>
    </div>
    </div>
    <nav class="flex items-center space-x-4">
    <a href="#" class="text-gray-700 hover:text-gray-900">Trending Videos</a>
    <a href="#" class="text-gray-700 hover:text-gray-900">Notifications</a>
    <a href="#" class="text-gray-700 hover:text-gray-900">Profile Settings</a>
    </nav>
</header>

<main class="flex">
    <section class="flex-1 p-4">
    <h2 class="text-xl font-bold mb-4">Subscribed Channel's Videos</h2>
    <!-- Subscribed channels videos list -->
    <h2 class="text-xl font-bold mb-4">Recommended Videos</h2>
    <!-- Recommended videos list -->
    </section>
    <aside class="w-64 bg-white p-4">
    <h3 class="font-bold mb-2">Library</h3>
    <!-- Library items -->
    <h3 class="font-bold mb-2">Subscriptions</h3>
    <!-- Subscriptions list -->
    <h3 class="font-bold mb-2">Saved Playlists</h3>
    <!-- Saved playlists list -->
    </aside>
</main>

<footer class="bg-white shadow p-4 text-center">
    <p>&copy; 2023 YouTube, LLC</p>
</footer>

</body>
</html>
"""

# Encoding
encoded_html = base64.b64encode(html_string.encode("utf-8")).decode("utf-8")

# Decoding
decoded_html = base64.b64decode(encoded_html).decode("utf-8")

print("Original HTML:", html_string)
print("Encoded HTML:", encoded_html)
print("Decoded HTML:", decoded_html)
print("Are they equal?", html_string == decoded_html)
