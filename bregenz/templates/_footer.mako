<%block name='footer'>
% if util.route_name == 'publication':
<div class="ui inverted vertical segment">
  <div class="ui center aligned container">
    <div class="ui stackable inverted divided grid">

      <div class="three wide column">
        <h4 class="ui inverted header">Group 1</h4>
        <div class="ui inverted link list">
          <a class="item" href="#">Link One</a>
          <a class="item" href="#">Link Two</a>
          <a class="item" href="#">Link Three</a>
          <a class="item" href="#">Link Four</a>
        </div>
      </div>

      <div class="three wide column">
        <h4 class="ui inverted header">Group 2</h4>
        <div class="ui inverted link list">
          <a class="item" href="#">Link One</a>
          <a class="item" href="#">Link Two</a>
          <a class="item" href="#">Link Three</a>
          <a class="item" href="#">Link Four</a>
        </div>
      </div>

      <div class="three wide column">
        <h4 class="ui inverted header">Group 3</h4>
        <div class="ui inverted link list">
          <a class="item" href="#">Link One</a>
          <a class="item" href="#">Link Two</a>
          <a class="item" href="#">Link Three</a>
          <a class="item" href="#">Link Four</a>
        </div>
      </div>

      <div class="seven wide column">
        <h4 class="ui inverted header">Footer Header</h4>
        <p>Extra space for a call to action isnide the footer that could help re-engage users.</p>
      </div>
    </div>

    <div class="ui inverted section divider"></div>
    <img class="ui centered mini image" src="${util.static_url('img/scrolliris-logo.png')}">

    <div class="ui horizontal inverted small divided link list">
      <a class="item" href="#">Site Map</a>
      <a class="item" href="#">About</a>
      <a class="item" href="#">Terms and Conditions</a>
      <a class="item" href="#">Privacy Policy</a>
    </div>
  </div>
</div>
% endif
</%block>
