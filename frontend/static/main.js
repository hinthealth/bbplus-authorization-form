/**
 * Establish the bbform namespace to avoid namespace conflicts.
 */
var bbform = bbform || {};


/**
 * Sets whether to enable or disable the "sample application" notice.
 * @param {boolean} enabled Whether to enable the "sample application" notice.
 */
bbform.setNoticeEnabled = function(enabled) {
  if (enabled) {
    $('#sample-notice').fadeIn(550);
  } else {
    $('#sample-notice').fadeOut(550);
  }
};


/**
 * Sends an RPC to save a frequency.
 * @param {string} frequency Frequency to save.
 */
bbform.saveFrequency = function(frequency) {
  $.ajax({
    'url': '/api/update_frequency',
    'type': 'POST',
    'data': {
      'frequency': frequency
    },
    'error': function(e) {
      alert('An error occurred saving.');
    },
    'success': function(e) {
      window.location = window.location.href = '/?saved';
    },
  });
};


/**
 * Sends an RPC to remove a direct address.
 * @param {string} directAddress Direct address to remove.
 */
bbform.removeDirectAddress = function(directAddress) {
  $.ajax({
    'url': '/api/remove_direct_address',
    'type': 'POST',
    'data': {
      'direct_address': directAddress
    },
    'error': function(e) {
      alert('An error occurred removing this Direct address.');
    },
    'success': function(e) {
      window.location = window.location.href = '/?saved';
    },
  });
};


/**
 * Callback for clicking upon the window.
 */
bbform.onWindowClick_ = function(e) {
  if (!e.target.hasAttribute('data-action')) {
    return;
  };
  switch(e.target.getAttribute('data-action')) {
    case 'add-direct-address':
      break;
    case 'remove-direct-address':
      bbform.removeDirectAddress(e.target.getAttribute('data-value'));
      break;
    case 'save-frequency':
      var frequency = $('input[name="frequency"]:checked').val();
      bbform.saveFrequency(frequency);
      break;
    case 'remove-notice':
      bbform.setNoticeEnabled(false);
  };
};


/**
  * Initializes events on the page.
  */
bbform.init = function() {
  window.addEventListener('click', bbform.onWindowClick_);
};
