<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <meta name="description" content="${_('meta.description')}">
    <meta name="author" content="${_('meta.author')}">
    <meta name="keywords" content="${_('meta.keywords')}">
    <title><%block name='title'/></title>
    <link rel="shortcut icon" type="image/x-icon" href="${req.route_url('index') + 'favicon.ico'}">
    <link rel="icon" type="image/x-icon" sizes="16x16 32x32 48x48 64x64 96x96 128x128 192x192" href="/favicon.ico">
    <link rel="apple-touch-icon" type="image/png" sizes="180x180" href="${req.util.static_path('img/touch-icon-180.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="167x167" href="${req.util.static_path('img/touch-icon-167.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="152x152" href="${req.util.static_path('img/touch-icon-152.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="120x120" href="${req.util.static_path('img/touch-icon-120.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="76x76" href="${req.util.static_path('img/touch-icon-76.png')}">
    <link rel="apple-touch-icon" type="image/png" sizes="57x57" href="${req.util.static_path('img/touch-icon-57.png')}">
    <link rel="icon" type="image/png" sizes="192x192" href="${req.util.static_path('img/favicon-192.png')}">
    <link rel="icon" type="image/png" sizes="128x128" href="${req.util.static_path('img/favicon-128.png')}">
    <link rel="icon" type="image/png" sizes="96x96" href="${req.util.static_path('img/favicon-96.png')}">
    <link rel="icon" type="image/png" sizes="64x64" href="${req.util.static_path('img/favicon-64.png')}">
    <link rel="icon" type="image/png" sizes="48x48" href="${req.util.static_path('img/favicon-48.png')}">
    <link rel="icon" type="image/png" sizes="32x32" href="${req.util.static_path('img/favicon-32.png')}">
    <link rel="icon" type="image/png" sizes="16x16" href="${req.util.static_path('img/favicon-16.png')}">
    <link rel="author" type="text/plain" href="/humans.txt">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300|Roboto+Slab:300" rel="stylesheet">
    <link rel="stylesheet" href="${req.util.hashed_asset_url('master.css')}">
    <style>body{background-color:#ffffff;}</style>
    <style>.not-ready{visibility:hidden;}</style>
    <script><%include file='willisau:assets/_fouc.js'/></script>
  </head>
  <body id="application">
    <div id="wrapper">
      <header>
        <%block name='header'>
        <%include file='_header.mako'/>
        </%block>
      </header>

      <main>
        <div class="content">
        ${self.body()}
        </div>
      </main>

      <footer>
        <%block name='footer'>
        <%include file='_footer.mako'/>
        </%block>
      </footer>
    </div>

    <%def name="add_icons(svg_file)">
    ## img/FILE.[hash].svg
    <% svg_path = req.util.manifest_json.get(svg_file, 'img/' + svg_file) %>
    <%include file='willisau:../static/${svg_path}'/>
    </%def>

    <svg xmlns="http://www.w3.org/2000/svg" style="display:none;">
    <% add_icons('master.svg') %>
    </svg>

    <%block name='script'>
    <script src="${util.hashed_asset_url('master.js')}" charset="utf-8"></script>
    </%block>
    <%block name='extra_script'/>
  </body>
</html>
