"""Custom logger."""
import logging


class BaseLogger(logging.Logger):

    """A logger with custom log functions."""

    def i(self, msg, *args, **kwargs):
        """Utility function equivalent to info()."""
        super(BaseLogger, self).info(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        """Utility function equivalent to warning()."""
        super(BaseLogger, self).warning(msg, *args, **kwargs)

    def d(self, msg, *args, **kwargs):
        """Utility function equivalent to debug()."""
        super(BaseLogger, self).debug(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        """Utility function equivalent to error()."""
        super(BaseLogger, self).error(msg, *args, **kwargs)

    def c(self, msg, *args, **kwargs):
        """Utility function equivalent to critical()."""
        super(BaseLogger, self).critical(msg, *args, **kwargs)

    def ex(self, msg, *args, **kwargs):
        """Utility function equivalent to exception()."""
        super(BaseLogger, self).exception(msg, *args, **kwargs)

    def vomit(self, msg, *args, **kwargs):
        """Utility function equivalent to exception()."""
        super(BaseLogger, self).d(msg, *args, **kwargs)


class GmailSMTPHandler(logging.handlers.SMTPHandler):

    """Gmail smtp handler."""

    def emit(self, record):
        """Format a record and send it to specified addresses."""
        try:
            import smtplib
            import string
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                string.join(self.toaddrs, ","),
                self.getSubject(record),
                formatdate(), msg
                )
            if self.username:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
