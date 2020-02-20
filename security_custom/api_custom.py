# -*- coding: utf-8 -*-

from odoo import api


def call_kw_model(method, self, args, kwargs):
    context, args, kwargs = api.split_context(method, args, kwargs)
    recs = self.with_context(context or {})
    api._logger.debug("call %s.%s(%s)", recs, method.__name__, api.Params(args, kwargs))
    result = method(recs, *args, **kwargs)

    clear_method = getattr(type(self.env['ir.rule']), 'clear_caches')

    clear_method()

    return api.downgrade(method, result, recs, args, kwargs)


def call_kw_multi(method, self, args, kwargs):
    ids, args = args[0], args[1:]
    context, args, kwargs = api.split_context(method, args, kwargs)
    recs = self.with_context(context or {}).browse(ids)
    api._logger.debug("call %s.%s(%s)", recs, method.__name__, api.Params(args, kwargs))
    result = method(recs, *args, **kwargs)

    clear_method = getattr(type(self.env['ir.rule']), 'clear_caches')

    clear_method()

    return api.downgrade(method, result, recs, args, kwargs)


api.call_kw_model = call_kw_model
api.call_kw_multi = call_kw_multi
