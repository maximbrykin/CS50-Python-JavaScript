document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').addEventListener('submit', send_email);

});


  

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Show the Mailbox content
  
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // Create div for the emails list
    const div1 = document.createElement('div')
    div1.id = 'emails-table'
    document.querySelector('#emails-view').append(div1);
    // For each email
    emails.forEach(email => {
      console.log(email);

      // Create div for each email
      const div_email = document.createElement('div')
      div_email.className = 'emails-list'
      // Mark grey if an email is read
      if (email.read === true) div_email.className += ' read'
      // Add an email to the list
      if (mailbox === 'sent') 
      div_email.innerHTML = 'To: <strong>' + email.recipients + '</strong> Subject: <strong>' + email.subject + '</strong> Time: <strong>' + email.timestamp + '</strong>'
      else
      div_email.innerHTML = 'From: <strong>' + email.sender + '</strong> Subject: <strong>' + email.subject + '</strong> Time: <strong>' + email.timestamp + '</strong>'
      document.querySelector('#emails-table').append(div_email); 
      
      // Go to Show an email content
      div_email.addEventListener('click', function() {
        read_email(email.id)
        get_email(email.id)
      });

    });
  });
  

}

function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  load_mailbox('sent');
}

function get_email(email_id) {
fetch('/emails/'+email_id)
.then(response => response.json())
.then(email => {
    // Print email
    console.log(email);

  // Hide other divs
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  
  // Display an email
  document.querySelector('#email-view').innerHTML = 'To: <strong>' + email.recipients + '</strong><br>'
  document.querySelector('#email-view').innerHTML += 'From: <strong>' + email.sender + '</strong><br>'
  document.querySelector('#email-view').innerHTML += 'Subject: <strong>' + email.subject + '</strong><br>'
  document.querySelector('#email-view').innerHTML += 'Time: <strong>' + email.timestamp + '</strong><br>'
  document.querySelector('#email-view').innerHTML += email.body
});
}

function read_email(email_id) {
  fetch('/emails/'+email_id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive_email(email_id) {
  fetch('/emails/'+email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  load_mailbox('inbox');
}

function unarchive_email(email_id) {
  fetch('/emails/'+email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  load_mailbox('inbox');
}

function reply_email(email_id) {
  fetch('/emails/'+email_id)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
  
      // ... do something else with email ...
  });
  }