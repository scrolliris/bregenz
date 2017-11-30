<%inherit file='_layout.mako'/>

<%block name='title'>Try Scrolliris</%block>

<%block name='footer'>
</%block>

<% content = render_content() %>

<div class="grid">
  <div class="secondary nav row">
    <div class="column-12">
      <div class="breadcrumb">
        <a class="item" href="/">Concepts of science and knowledge</a>
        <span class="divider">&gt;</span>
        <span class="active item">${content['title']}</span>
      </div>
    </div>

    <%def name="render_icon(name, view_box='0 0 8 8', width=20, height=20)">
      <svg class="icon ${name}" viewBox="${view_box}" width="${width}" height="${height}">
      <use xlink:href="#open-iconic.min_${name}" class="icon ${name}"></use>
      </svg>
    </%def>

    <div class="column-4">
      <div class="options">
        <a class="item disabled mobile hidden"><% render_icon('cog') %></a>
        <a class="item disabled"><% render_icon('bookmark') %></a>
        <span class="divider mobile hidden"></span>
        <a class="item disabled mobile hidden"><% render_icon('fullscreen-enter') %></a>
        <a class="item disabled mobile hidden"><% render_icon('text') %></a>
      </div>
    </div>
  </div>

  <div class="row">
    <div class="article-container offset-4 column-8 offset-l-1 column-l-14">
      <%block name='announcement'>
      <%
        msg = (req.session.pop_flash('announcement') or [None])[0]
      %>
      % if msg:
        <div class="warning message" role="alert">
          <div class="header">NOTICE</div>
          <p>${msg}</p>
        </div>
      % endif
      </%block>

      <%def name="render_article()">
        <%
          import hashlib

          def authors_with_avator(authors):
              m = hashlib.md5()
              for a in content['authors']:
                  author = ''
                  if 'mail' in a and a['mail']:
                      m.update(a['mail'])
                      author += '<img class="avatar" src="https://www.gravatar.com/avatar/{}.jpg?s=32">'.format(m.hexdigest())
                  author += '<span class="rounded label name">{}</span>'.format(a['name'])
                  yield author
        %>
        <article>
          <h1 class="title">${content['title']}</h1>
          <div class="extra info">
            <div class="author">${',&nbsp;'.join(authors_with_avator(content['authors']))|n,trim}</div>
            <div class="published_at">published in <span class="class">Concepts of science and knowledge</span></div>
            <div class="badge">
              <a href="https://about.scrolliris.com/"><img src="https://img.scrolliris.io/badge/tracking/on.svg" alt="tracking status"></a>
            </div>
          </div>
          <p class="outline">${content['outline']}</p>
          <div id="content" class="body">
            ${content['body']|n,trim,clean(tags=['h2', 'h3', 'p', 'a', 'br', 'ul', 'ol', 'li', 'code'])}
          </div>
        </article>

        <div class="meta">
          <span class="license primary label">${content['license']}</span>
          <p class="copy">&copy;${content['copyright']}</p>
        </div>
      </%def>

      ## cache (seconds) 60 * 60 * 24 * 7 = 604800
      % if util.is_production and util.cache_article:
        <%block cached='True' cache_timeout='604800' cache_type='memory'>
          ${render_article()}
        </%block>
      % else:
        <%block cached='False'>
          ${render_article()}
        </%block>
      % endif
      </div>
    </div>
  </div>
</div>

<%block name='extra_script'>
<script>
// tracker client script
(function(d, w) {
  var config = {
        projectId: '${util.scrolliris_project_id}'
      , apiKey: '${util.scrolliris_write_key}'
      }
    , settings = {
        endpointURL: 'https://api.scrolliris.io/v1.0/projects/'+config.projectId+'/events/read'
      }
    , options = {}
    ;
    var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://script.scrolliris.io/projects/'+c.projectId+'/tracker.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityTracker,t=(new r.Client(c,settings));t.ready(['body'],function(){t.record(options);});}catch(_){}};s.parentNode.insertBefore(k,s);
}(document, window));

// reflector canvas widget
(function(d, w) {
  var config = {
        projectId: '${util.scrolliris_project_id}'
      , apiKey: '${util.scrolliris_read_key}'
      }
    , settings = {
        endpointURL: 'https://api.scrolliris.io/v1.0/projects/'+config.projectId+'/results/read?api_key='+config.apiKey
      }
    , options = {
        widget: 'inactive'
      }
    ;

  var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://widget.scrolliris.io/projects/'+c.projectId+'/reflector.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityReflector,t=(new r.Widget(c,{settings:settings,options:options}));t.render();}catch(_){}};s.parentNode.insertBefore(k,s);
})(document, window);
</script>
</%block>
