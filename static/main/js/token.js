// Document Dot Ready
$(document).ready(function() {

    // steal token from url
    var oauthHash = location.hash.substr(1);
    var accessToken = oauthHash.substr(oauthHash.indexOf('access_token=')).split('&')[0].split('=')[1];
    console.log('oauth:' + accessToken);

    // do some stuff
    if (accessToken) {
        $('#access-token').val('oauth:' + encodeURIComponent(accessToken));
    }

});
