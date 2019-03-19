#!/usr/bin/env python
# coding: utf-8

# In[1]:


Status RenameOp(const GraphDef& input_graph_def,
                const TransformFuncContext& context,
                GraphDef* output_graph_def) {
  if (!context.params.count("old_op_name") ||
      (context.params.at("old_op_name").size() != 1) ||
      get_ipython().system('context.params.count("new_op_name") ||')
      (context.params.at("new_op_name").size() != 1)) {
    return errors::InvalidArgument(
        "remove_nodes expects exactly one 'old_op_name' and 'new_op_name' "
        "argument, e.g. rename_op(old_op_name=Mul, new_op_name=Multiply)");
  }

  const string old_op_name = context.params.at("old_op_name")[0];
  const string new_op_name = context.params.at("new_op_name")[0];
  output_graph_def->Clear();
  for (const NodeDef& node : input_graph_def.node()) {
    NodeDef* new_node = output_graph_def->mutable_node()->Add();
    new_node->CopyFrom(node);
    if (node.op() == old_op_name) {
      new_node->set_op(new_op_name);
    }
  }

  return Status::OK();
}


# In[ ]:




