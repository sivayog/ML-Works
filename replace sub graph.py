#!/usr/bin/env python
# coding: utf-8

# In[1]:


TF_RETURN_IF_ERROR(ReplaceMatchingOpTypes(
    input_graph_def,  // clang-format off
    {"Conv2D",
        {
            {"ResizeBilinear"},
            {"*"}
        }
    },  // clang-format on
    [](const NodeMatch& match, const std::set<string>& input_nodes,
       const std::set<string>& output_nodes,
       std::vector<NodeDef>* new_nodes) {
      // Find all the nodes we expect in the subgraph.
      const NodeDef& conv_node = match.node;
      const NodeDef& resize_node = match.inputs[0].node;
      const NodeDef& weights_node = match.inputs[1].node;

      // We'll be reusing the old weights.
      new_nodes->push_back(weights_node);

      (/, Create, a, 'no-op', mirror, padding, node, that, has, no, effect.)
      NodeDef pad_dims_node;
      pad_dims_node.set_op("Const");
      pad_dims_node.set_name(conv_node.name() + "_dummy_paddings");
      SetNodeAttr("dtype", DT_INT32, &pad_dims_node);
      SetNodeTensorAttr<int32>("value", {4, 2}, {0, 0, 0, 0, 0, 0, 0, 0},
                               &pad_dims_node);
      new_nodes->push_back(pad_dims_node);

      (/, Set, up, the, new, fused, version, of, the, convolution, op.)
      NodeDef fused_conv;
      fused_conv.set_op("FusedResizeAndPadConv2D");
      fused_conv.set_name(match.node.name());
      AddNodeInput(resize_node.input(0), &fused_conv);
      AddNodeInput(resize_node.input(1), &fused_conv);
      AddNodeInput(pad_dims_node.name(), &fused_conv);
      AddNodeInput(conv_node.input(1), &fused_conv);
      CopyNodeAttr(resize_node, "align_corners", "resize_align_corners",
                   &fused_conv);
      SetNodeAttr("mode", "REFLECT", &fused_conv);
      CopyNodeAttr(conv_node, "T", "T", &fused_conv);
      CopyNodeAttr(conv_node, "padding", "padding", &fused_conv);
      CopyNodeAttr(conv_node, "strides", "strides", &fused_conv);
      new_nodes->push_back(fused_conv);

      return Status::OK();
    },
    {}, &replaced_graph_def));


# In[ ]:




