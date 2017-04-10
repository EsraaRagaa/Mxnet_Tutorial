# -*- coding: utf-8 -*-
import mxnet as mx
import numpy as np
import data_preprocessing as dp
import logging
logging.basicConfig(level=logging.INFO)

def LottoNet(epoch,batch_size,save_period):

    '''data processing'''

    #training data,#test_data
    training_data,test_data,normalization_factor = dp.data_preprocessing()
    tr_i, tr_o = zip(*training_data)
    train_iter = mx.io.NDArrayIter(data={'input' : np.asarray(tr_i)}, label={'output':np.asarray(tr_o)}, batch_size=batch_size,shuffle=True)
    test_iter = mx.io.NDArrayIter(data={'input': test_data})

    '''neural network feedforward'''

    input = mx.sym.Variable('input')
    label = mx.sym.Variable('output')

    affine1 = mx.sym.FullyConnected(data=input,name='fc1',num_hidden=100)
    hidden1 = mx.sym.Activation(data=affine1, name='sigmoid1', act_type="sigmoid")

    affine2 = mx.sym.FullyConnected(data=hidden1, name='fc2', num_hidden=100)
    hidden2 = mx.sym.Activation(data=affine2, name='sigmoid2', act_type="sigmoid")

    affine3 = mx.sym.FullyConnected(data=hidden2, name='fc3', num_hidden=100)
    hidden3 = mx.sym.Activation(data=affine3, name='sigmoid3', act_type="sigmoid")

    affine4 = mx.sym.FullyConnected(data=hidden3, name='fc4', num_hidden=100)
    hidden4 = mx.sym.Activation(data=affine4, name='sigmoid4', act_type="sigmoid")

    out_affine = mx.sym.FullyConnected(data=hidden4, name='out_fc', num_hidden=6)

    output = mx.sym.LinearRegressionOutput(data=out_affine, label=label)
    #output = mx.sym.LogisticRegressionOutput(data=out_affine , label=label)

    '''
    #print output.list_arguments()
    model = mx.model.FeedForward(
        symbol=output,  # network structure
        num_epoch=10000,  # number of data passes for training
        learning_rate=0.1  # learning rate of SGD
    )
    model.fit(
        X=train_iter,  # training data  # validation data
        batch_end_callback=mx.callback.Speedometer(batch_size, 50)  # output progress for each 200 data batches
    )
    print model.predict(test_iter)*45
    '''
    print output.list_arguments()
    #weights save
    model_name = 'weights/Lotto_Net'
    checkpoint = mx.callback.do_checkpoint(model_name,period=save_period)

    mod = mx.mod.Module(symbol=output, data_names = ["input"], label_names = ["output"] ,context = mx.gpu())

    # Network information print
    print mod.data_names
    print mod.label_names
    print train_iter.provide_data
    print train_iter.provide_label

    #the below code already is declared by mod.fit function, thus we don't have to write it.
    #mod.bind(data_shapes=train_iter.provide_data,label_shapes=train_iter.provide_label)

    '''
    # When you want to load the saved weights, uncomment the code below.
    symbol, arg_params, aux_params = mx.model.load_checkpoint(model_name, 50000)

    #the below code needs mod.bind, but If arg_params and aux_params is set in mod.fit, you do not need the code below, nor do you need mod.bind.
    # mod.set_params(arg_params, aux_params)
    '''

    mod.fit(train_iter,
            optimizer='adam',
            optimizer_params={'learning_rate': 0.001},
            initializer=mx.initializer.Xavier(rnd_type='gaussian', factor_type="avg", magnitude=1),
            eval_metric=mx.metric.MSE(),
            num_epoch=epoch,
            arg_params= None,
            aux_params=None,
            epoch_end_callback=checkpoint)

    print mod.data_shapes
    print mod.label_shapes,
    print mod.output_shapes
    print mod.get_params()
    print mod.get_outputs()
    print mod.score(train_iter, ['mse', 'acc'])

    result = mod.predict(train_iter).asnumpy()
    result1 = np.round(result*normalization_factor)
    result2 = np.rint(result*normalization_factor)
    #print result1
    #print result2

    mod.bind(data_shapes=test_iter.provide_data,label_shapes=None,force_rebind=True)

    '''Annotate only when running test data.'''
    # mod.set_params(arg_params, aux_params)

    result=mod.predict(test_iter)
    result1 = mx.nd.round(normalization_factor*result)
    result2 = mx.nd.rint(normalization_factor*result)

    result1 = result1.asnumpy()
    result2 = result2.asnumpy()
    #print result1
    #print result2

    return [result1,result2]

if __name__=="__main__":
    print "NeuralNet_starting in main"
    net=LottoNet(epoch=100,batch_size=10,save_period=1000)
    print net[0]
    print net[1]
else:
    print "NeuralNet_imported"