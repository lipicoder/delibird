"""Context management for Delibird."""

from contextvars import ContextVar, Token


class Context:
    """Context class to manage the context of the application.

    forbid mutation while providing a context manager with contextvar
    """

    # static element belongs to class
    __var__: ContextVar
    _token: Token

    def __enter__(self):
        """Enter the context."""
        if self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context enter called without an exit."
            )

        # context enter will return context instance with a token
        self._token = self.__var__.set(self)
        return self

    def __exit__(self, *_):
        """Exit the context."""
        if not self._token:
            raise RuntimeError(
                "Asymmetric use of context. Context exit called without an enter."
            )
        # Reset the context variable to the value it had before the
        # ContextVar.set() that created the token was used.
        self.__var__.reset(self._token)

        # reset token
        self._token = Token()

    @classmethod
    def get(cls):
        """Get the context instance."""
        return cls.__var__.get()