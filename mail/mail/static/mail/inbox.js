document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


  

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  // On button Send click - Send Email
  document.querySelector('#compose-form').addEventListener('submit', send_email);
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
    const div1 = document.createElement('div');
    div1.id = 'emails-table';
    document.querySelector('#emails-view').append(div1);
    // For each email
    emails.forEach(email => {
      console.log(email);

      // Create div for each email
      const div_email = document.createElement('div');
      div_email.className = 'emails-list row';
      // Mark grey if an email is read
      if (email.read === true) div_email.className += ' read';
      // Add an email to the list
      if (mailbox === 'sent') 
      div_email.innerHTML = '<div class="col-sm-3">' + email.recipients + '</div> <div class="col-sm-7">' + email.subject + '</div> <div class="col-sm-2">' + email.timestamp + '</div>';
      else
      div_email.innerHTML = '<div class="col-sm-3">' + email.sender + '</div> <div class="col-sm-7">' + email.subject + '</div> <div class="col-sm-2">' + email.timestamp + '</div>';
      document.querySelector('#emails-table').append(div_email); 
      
      // Go to Show an email content
      div_email.addEventListener('click', function() {
        read_email(email.id);
        get_email(email.id);
      });
    });
  });
}

function send_email(event) {
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
  })
  .then(() => {
    load_mailbox('sent')
  });
  event.preventDefault();
}

function get_email(email_id) {
fetch('/emails/'+email_id)
.then(response => response.json())
.then(email => {
    // Print email
    console.log(email);
    const user = document.querySelector("h2").innerHTML
  // Hide other divs
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  
  // Display an email
  document.querySelector('#email-view').innerHTML = '<strong>From: </strong>' + email.sender + '<br>';
  document.querySelector('#email-view').innerHTML += '<strong>To: </strong>' + email.recipients + '<br>';
  document.querySelector('#email-view').innerHTML += '<strong>Subject: </strong>' + email.subject + '<br>';
  document.querySelector('#email-view').innerHTML += '<strong>Timestamp: </strong>' + email.timestamp;
  document.querySelector('#email-view').innerHTML += '<hr>' + email.body + '<br>';

  // Reply button
  const reply_button = document.createElement('button');
  reply_button.id = "reply-button";
  reply_button.innerHTML = "Reply";
  reply_button.className = "btn btn-primary";
  document.querySelector('#email-view').append(reply_button);
  document.querySelector('#reply-button').addEventListener('click', () => reply_email(email.sender, email.subject, email.body, email.timestamp));

  // Archive/Unarchive button
  const archive_button = document.createElement('button');
  archive_button.id = "archive-button";
  // Exclude Sent emails
  if ((email.sender !== user)) { 
    if (email.archived === false) {
      archive_button.innerHTML = "Archive";
      archive_button.className = "btn btn-secondary";
      document.querySelector('#email-view').append(archive_button);
      document.querySelector('#archive-button').addEventListener('click', () => archive_email(email.id));
    }
    else {
      archive_button.innerHTML = "Unarchive";
      archive_button.className = "btn btn-success";
      document.querySelector('#email-view').append(archive_button);
      document.querySelector('#archive-button').addEventListener('click', () => unarchive_email(email.id));
    }
  }

  
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
  .then(() => {
    load_mailbox('inbox')
  });
}

function unarchive_email(email_id) {
  fetch('/emails/'+email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(() => {
    load_mailbox('inbox')
  });
}

function reply_email(reply_recipients, reply_subject, reply_body, reply_date) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  
  // Reply content
  document.querySelector('#compose-recipients').value = reply_recipients;
  if (reply_subject.slice(0, 4) !== 'Re: ') {
    document.querySelector('#compose-subject').value = 'Re: ' + reply_subject;
  }
  else {
    document.querySelector('#compose-subject').value = reply_subject;
  }
  document.querySelector('#compose-body').value = '\n ------------------ \n On ' + reply_date + ' ' + reply_recipients + ' wrote: \n' + reply_body;

  // On button Send click - Send Email
document.querySelector('#compose-form').addEventListener('submit', send_email);
}
