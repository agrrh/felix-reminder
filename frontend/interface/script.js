var api_base_url = "http://127.0.0.1:8080";

var frontend = {version: "local"};
var year = 2021;

var app = {
  telegram_bot: "felix_kisovsky_test_bot",
  telegram_bot_name: "Felix TEST",
  github_url: "https://github.com/agrrh/felix-reminder",
  github_repo: "agrrh/felix-reminder"
};

function app_run(backend) {
  user_uuid = window.location.hash;

  jQuery.getJSON(api_base_url + "/users/" + user_uuid.replace('#', ''))
    .done(function() {
      $('.app-stage-ready').removeClass('visually-hidden');
    })
    .fail(function() {
      $('.app-stage-empty').removeClass('visually-hidden');

      var tpl_data = {app: app, backend: backend};
      $("#result-stage-empty").html(
        $.templates("#tpl-stage-empty").render(tpl_data)
      );
    })
    .always(function(data) {
      var tpl_data = {year: year, user: data, app: app};
      $("#result-header-user").html(
        $.templates("#tpl-header-user").render(tpl_data)
      );
    });
}

function app_init() {
  jQuery.getJSON(api_base_url + "/status")
    .done(function(data) {
      // Draw footer
      var tpl_data = {app: app, backend: data, frontend: frontend};
      $("#result-footer-status").html(
        $.templates("#tpl-footer-status").render(tpl_data)
      );

      // Draw contents
      app_run();
    })
    .fail(function() {
      $('.app-stage-error').removeClass('visually-hidden');
    })
    .always(function() {
      $('.app-stage-init').addClass('visually-hidden');
    });
}

function visuals_init() {
  document.getElementById("result-footer-year").innerHTML = new Date().getFullYear();
}

function main() {
  visuals_init();

  app_init();
}

// Start

main();
