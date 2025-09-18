# encoding: utf-8
"""
Various utility classes used internally by the package.
"""

# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import typing as _t

import warnings as _warnings


class _StaticClassMeta(type):
	"""
	Due to the "global state" nature of OpenGL, some of the classes need to have only a single instance.

	To have a truly static class (and not a singleton), with static properties,
	while also NOT polluting the class with ``@staticmethod`` and ``@classmethod`` decorators,
	let's just define the entire static class with its corresponding metaclass... which inherits from this one.

	Yes, it causes a few extra lines of boilerplate (each class is defined twice: as it's meta and an empty actual class),
	but this way we guarantee that each such static class is the only one.
	"""
	def __new__(mcls, name: str, bases: tuple[type], attrs: dict[str, _t.Any], **kwargs):
		try:
			# noinspection PyUnresolvedReferences
			cls = mcls.__single_instance  # The private field will be unique for each inheriting metaclass
		except AttributeError:
			cls = None

		if cls is not None:
			cls_repr = name
			if '__module__' in attrs:
				cls_repr = '{}.{}'.format(attrs['__module__'], name)
			cls_repr = f"<class {cls_repr!r}>"
			_warnings.warn(
				f"{cls_repr} attempts to become a second instance of {mcls!r}.\n"
				f"Only one can exist. {cls_repr} is just an alias for {cls!r}"
			)
			return cls

		cls = super().__new__(mcls, name, bases, attrs, **kwargs)
		cls.__init__ = mcls.__init_raising_error  # Explicitly forbid instantiating a static class
		cls._init_class()
		mcls.__single_instance = cls
		return cls

	def __init_raising_error(self, *args, **kwargs):
		"""Shared ``__init__`` method for all the static classes."""
		raise NotImplementedError(f"{self.__class__} is a static class and cannot be instantiated")

	def _init_class(cls):
		"""Each metaclass defines the initialization of its static class here."""
		pass
