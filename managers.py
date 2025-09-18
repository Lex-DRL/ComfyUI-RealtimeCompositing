# encoding: utf-8
"""
"""

# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import typing as _t

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import moderngl

from ._internal_classes import _StaticClassMeta


class ShaderPool:
	"""
	Each shader should ideally be compiled only once and reused for the entire lifetime of the python process.
	This class handles that.
	"""
	pass


class TexturePool:
	"""To improve performance, the underlying ModernGL texture objects are reused - with this class."""
	pass


class __GlobalManagerMeta(_StaticClassMeta):
	class __GlobalConfigMeta(_StaticClassMeta):
		pass  # GlobalConfig doesn't have any methods anyway - so let's define fields right there, for readability

	class GlobalConfig(metaclass=__GlobalConfigMeta):
		"""Global settings."""
		opengl_ver: int = 330

	del __GlobalConfigMeta  # It should never be used again

	def _init_class(cls):
		cls.__context: moderngl.Context = moderngl.create_standalone_context(require=cls.GlobalConfig.opengl_ver)
		cls.__pool_shaders = ShaderPool()
		cls.__pool_textures = TexturePool()

	@property
	def context(cls) -> moderngl.Context:
		"""Global OpenGL context"""
		return cls.__context

	@property
	def pool_shaders(self) -> ShaderPool:
		"""Shader cache."""
		return self.__pool_shaders

	@property
	def pool_textures(self) -> TexturePool:
		"""Texture cache - for reuse between render calls."""
		return self.__pool_textures


class GlobalManager(metaclass=__GlobalManagerMeta):
	"""
	Global rendering manager on top of ModernGL.

	Handles rendering context and optimized resource allocation.
	"""
	pass

del __GlobalManagerMeta  # It should never be used again
